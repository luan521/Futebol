import os
from datetime import datetime, date, timedelta
from unidecode import unidecode
import json
import pyspark.sql.functions as F
from cafu.utils.etl.datalake import proximas_partidas
from cafu.metadata.campeonatos_dafabet import campeonato_dafabet
from cafu.queries.odds import GetOdds
from cafu.metadata.paths import path
path_datalake = path('datalake')

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def update_odds(spark):
    """
    Atualiza datalake.odds
    
    .. figure:: ../../../imagens_doc/esquema_atualizacao.jpg
    
    Args:
        spark: (spark session) 
    """
    
    logging.info("INFO etl.data_lake.partidas_campeonato.update_partidas: "
                 "Function started")
    
    # campeonatos que terão jogos, hoje ou amanhã
    pr_part = proximas_partidas()
    dafabet = campeonato_dafabet()
    after_tomorrow = date.today()+timedelta(days=2)
    campeonatos = []
    for c in pr_part:
        for t in pr_part[c]:
            try:
                prox_jogo = datetime.strptime(pr_part[c][t], '%Y-%m-%d').date()
                if (prox_jogo<=after_tomorrow) and (c in dafabet):
                    campeonatos.append([c,t])
            except:
                pass
            
    if len(campeonatos)==0:
        logging.info("INFO etl.data_lake.odds.update_odds: "
                     "No match today or tomorrow.")
        return
    
    # atualizando
    for c in campeonatos:
        stop = False
        index = 0
        while not stop:
            query = GetOdds()
            query.get_campeonato_dafabet(c[0])
            descricao_partida = query.join_link_odds_partida(index)
            if descricao_partida is not None:
                if (
                    ('Hoje' in descricao_partida['horario']) or
                    ('Amanhã' in descricao_partida['horario'])
                   ):
                    query.open_odds()
                    odds = query.get_odds()
                    if len(odds)==2: # garantido que a coleta foi bem sucedida
                        return
                    odds['time_casa'] = descricao_partida['time_casa']
                    odds['time_visitante'] = descricao_partida['time_visitante']
                    odds['horario'] = descricao_partida['horario']
                    odds['date_update'] = str(datetime.now())
                    nome_arquivo = (
                                    descricao_partida['time_casa']+
                                    ' vs ' +
                                    descricao_partida['time_visitante']+
                                    '.json'
                                   ).replace(' ','_').lower()
                    try:
                        with open(f'{path_datalake}/odds/{c[0]}/{c[1]}/{nome_arquivo}', 'w') as fp:
                            json.dump(odds, fp)
                            logging.info(f"INFO etl.data_lake.odds.update_odds: "
                                         f"Updated {c}.{descricao_partida['time_casa']} vs "
                                         f"{descricao_partida['time_visitante']}")
                    except:
                        try:
                            os.mkdir(f'{path_datalake}/odds/{c[0]}/{c[1]}')
                            with open(f'{path_datalake}/odds/{c[0]}/{c[1]}/{nome_arquivo}', 'w') as fp:
                                json.dump(odds, fp)
                            logging.info(f"INFO etl.data_lake.odds.update_odds: "
                                         f"Updated {c}.{descricao_partida['time_casa']} vs "
                                         f"{descricao_partida['time_visitante']}")
                        except Exception as err:
                            logging.error(f"ERROR etl.data_lake.odds.update_odds: "
                                          f"Could not update {c}.{descricao_partida['time_casa']} vs "
                                          f"{descricao_partida['time_visitante']}")
                            logging.error(err)
                elif descricao_partida['horario']!='ao vivo':
                    stop = True
            else:
                stop = True
            query.web.close() # encerra a sessão
            index+=1