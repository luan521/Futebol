import re
import time
from time import sleep
import json
from datetime import datetime
from tqdm import tqdm
from cafu.utils import WebdriverChrome
from cafu.utils.etl.datalake import jogos_ids_jogadores_desatualizados
from cafu.utils.string import convert_str_var_time
from cafu.queries.jogador import Bio
from cafu.metadata import get_schema
from cafu.metadata.paths import path
path_datalake = path('datalake')

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def find_id_jogadores(jogo_id):
    """
    Args:
        jogo_id: (int or str) completa o link https://www.espn.com.br/futebol/escalacoes?jogoId=<jogo_id>. 
    Returns:
        list: códigos dos jogadores que foram inscritos para a partida, referente ao <jogo_id>
    """
    
    init = time.time()
    
    try:
        web = WebdriverChrome()
        link_partida = f'https://www.espn.com.br/futebol/escalacoes?jogoId={str(jogo_id)}'
        web.web.get(link_partida)
        padrao = 'jogador/.+/id/[0-9]+/.+'
        links_0 = web.web.find_elements_by_tag_name('a')
        links = [l.get_attribute('href') for l in links_0]
        web.web.close()
        logging.info("P-1 SUCCESS etl.data_lake.jogadores_partida.find_id_jogadores: Links collected on match page")
    except:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.error(f"ERROR etl.data_lake.jogadores_partida.find_id_jogadores: "
                      f"Could not collect links on match page. <jogo_id>={jogo_id}. runtime = {runtime_str}")
        return
    
    ids_jogadores = []
    for l in links:
        try:
            id_ = re.findall(padrao, l)[0][13:]
            id_part1 = id_.split('/')[0]
            id_part2 = id_.split('/')[1]
            ids_jogadores.append({'id_part1': id_part1, 'id_part2': id_part2})
        except:
            pass
    
    if len(ids_jogadores) >= 22:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS etl.data_lake.jogadores_partida.find_id_jogadores: "
                     f"Function executed successfully. <jogo_id>={jogo_id}. runtime = {runtime_str}")
    else:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.error(f"ERROR etl.data_lake.jogadores_partida.find_id_jogadores: "
                      f"{len(ids_jogadores)} players were found. <jogo_id>={jogo_id}. runtime = {runtime_str}")
        return
    return ids_jogadores

def update_jogadores(spark):
    """
    Atualiza datalake.jogadores
    
    .. figure:: ../../../imagens_doc/esquema_atualizacao.png
    
    Args:
        spark: (spark session) 
    """
    
    logging.info("INFO etl.data_lake.jogadores_partida.update_jogadores: "
                 "Function started")
    
    partidas = jogos_ids_jogadores_desatualizados()
    if len(partidas)==0:
        logging.info("INFO etl.data_lake.jogadores_partida.update_jogadores: "
                     "Already up to date")
    for c in partidas:
        for t in partidas[c]:
            for jogo_id in partidas[c][t]:
                ids_jogadores = find_id_jogadores(jogo_id)
                for id_ in tqdm(ids_jogadores):
                    sleep(1)
                    jogador_id = f"{id_['id_part1']}/{id_['id_part2']}"
                    query = Bio(jogador_id)
                    
                    try:
                        time_temporadas = query.time(1)
                        time = time_temporadas[0]
                        qt_temporadas = int(time_temporadas[1].replace(' TEMPORADA', ''))
                    except Exception as err:
                        time = None
                        qt_temporadas = None
                        logging.error(f"ERROR etl.data_lake.jogadores_partida.update_jogadores: "
                                      f"Info (time, temporadas) with unexpected format. <jogador_id>={jogador_id}")
                        logging.error(err)
                    posicao = query.posicao()
                    try:
                        altura = float(query.altura().replace(' m', ''))
                    except Exception as err:
                        altura = None
                        logging.error(f"ERROR etl.data_lake.jogadores_partida.update_jogadores: "
                                      f"Info (altura) with unexpected format. <jogador_id>={jogador_id}")
                        logging.error(err)
                    try:
                        massa = float(query.massa().replace(' kg', ''))
                    except Exception as err:
                        massa = None
                        logging.error(f"ERROR etl.data_lake.jogadores_partida.update_jogadores: "
                                      f"Info (massa) with unexpected format. <jogador_id>={jogador_id}")
                        logging.error(err)
                    data_nascimento = query.data_nascimento()
                    try:
                        data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
                    except Exception as err:
                        logging.error(f"ERROR etl.data_lake.jogadores_partida.update_jogadores: "
                                      f"Info (data_nascimento) with unexpected format. <jogador_id>={jogador_id}")
                        logging.error(err)
                    nacionalidade = query.nacionalidade()
                    
                    query.web.close()

                    data = [
                            {
                             'jogo_id': int(jogo_id),
                             'jogador_id': jogador_id,
                             'time': time,
                             'qt_temporadas': qt_temporadas,
                             'posicao': posicao,
                             'altura': altura,
                             'massa': massa,
                             'data_nascimento': data_nascimento,
                             'nacionalidade': nacionalidade,
                             'date_update': datetime.now()
                            }
                           ]
                    schema = get_schema('jogadores')
                    df_jogador = spark.createDataFrame(data, schema=schema)
                    df_jogador.write.parquet(path_datalake+
                                             f'/jogadores/df_jogador', 
                                             mode='append')
                # atualizando datalake/metadata.json
                r = open(path_datalake+'/metadata.json')
                metadata = json.load(r) 
                try:
                    metadata['jogadores'][c][t][jogo_id] = 'evaluation'
                except:
                    metadata['jogadores'][c][t] = {}
                    metadata['jogadores'][c][t][jogo_id] = 'evaluation'
                with open(path_datalake+'/metadata.json', 'w') as fp:
                    json.dump(metadata, fp)
            logging.info(f"INFO etl.data_lake.jogadores_partida.update_jogadores: "
                         f"Updated <c>={c}, <t>={t}, <jogo_id>={jogo_id}")