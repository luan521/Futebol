import pandas as pd
import json
import time
from cafu.utils.etl.partidas_campeonato import id_left_right
from cafu.utils.string import convert_str_var_time
from cafu.metadata.campeonatos_espn import campeonato_espn
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def partidas_campeonato(pais_divisao, temporada):
    """
    Busca as partidas do campeonato, no site da ESPN
        
    Args:
        pais_divisao: (str) chave primária do dicionário campeonatos, caminho metadata/campeonatos_espn
        temporada: (str) chave secundária do dicionário campeonatos, caminho metadata/campeonatos_espn
    Returns:
         pandas dataframe: jogo_id, dates, rodada, time_casa, time_visitante
    """
    
    logging.info(f"INFO etl.data_lake.partidas_campeonato.partidas_campeonato: "
                 f"Function started. <pais_divisao>={pais_divisao}, <temporada>={temporada}")
    
    init = time.time()
    
    dados_campeonato = campeonato_espn(pais_divisao, temporada) 
    campeonato = dados_campeonato['nome']
    id_inicial =dados_campeonato['id']
    qt_jogos_rodada = dados_campeonato['qt_jogos_rodada']
    qt_partidas_campeonato = 2*qt_jogos_rodada*(2*qt_jogos_rodada-1)
    ids, partidas, dates = id_left_right(id_inicial, campeonato, qt_partidas_campeonato)
    ids, partidas, dates = id_left_right(id_inicial+1, campeonato, qt_partidas_campeonato,
                                         left=False, partidas=partidas, dates=dates, ids=ids)
    
    try:
        data = []
        for i in range(len(partidas)):
            data.append([ids[i], dates[i], partidas[i]])
        df = pd.DataFrame(data, columns=['jogo_id', 'dates', 'partida']).sort_values('jogo_id')
        df.index = range(df.shape[0])

        dates = []
        for i in range(0,df.shape[0], qt_jogos_rodada):
            median_date = df.iloc[i:i+qt_jogos_rodada].sort_values('dates')['dates'][i+int(qt_jogos_rodada/2)]
            dates_0 = [median_date for i in range(qt_jogos_rodada)]
            dates = dates+dates_0

        df['median_dates'] = dates

        df = df.sort_values(['median_dates'])
        rodadas = [i for i in range(1,(qt_jogos_rodada*2-1)*2+1) for j in range(qt_jogos_rodada)]
        df['rodada'] = rodadas
        df = df.drop('median_dates',axis=1)

        df = df.sort_values(['jogo_id'])

        df[['time_casa','time_visitante']] = pd.DataFrame(df['partida'].values.tolist(), index= df.index)
        df = df.drop('partida', axis=1)
        
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS etl.data_lake.partidas_campeonato.partidas_campeonato: Function executed successfully. "
                     f"<pais_divisao>={pais_divisao}, <temporada>={temporada}, <qt_jogos_rodada>={qt_jogos_rodada}. "
                     f"runtime = {runtime_str}")
        return df
    except Exception as err:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.error(f"ERROR etl.data_lake.partidas_campeonato.partidas_campeonato: Unexpected error: "
                      f"Could not execute function. <pais_divisao>={pais_divisao}, <temporada>={temporada}, "
                      f"<qt_jogos_rodada>={qt_jogos_rodada}. runtime = {runtime_str}")
        logging.error(err)
        return
    
def update_partidas_campeonato():
    """
    Atualiza datalake.jogos_ids
    """
    
    logging.info("INFO etl.data_lake.partidas_campeonato.update_partidas_campeonato: "
                 "Function started")
    
    # buscando campeonatos definidos no projeto
    campeonatos0 = campeonato_espn()
    campeonatos = [
                   [k1, k2] for k1 in list(campeonatos0.keys()) 
                            for k2 in list(campeonatos0[k1].keys())
                  ]
    
    # buscando campeonatos já atualizados
    r = open(path('datalake')+'/metadata.json')
    metadata = json.load(r)
    campeonatos_atualizados = [
                           [k1, k2] for k1 in list(metadata['jogos_ids'].keys()) 
                                    for k2 in list(metadata['jogos_ids'][k1].keys())
                                    if metadata['jogos_ids'][k1][k2] != 'failed'
                          ]
    
    # removendo campeonatos já atualizados
    for c in campeonatos_atualizados: campeonatos.remove(c)
    
    # atualizando campeonatos
    for c in campeonatos:
        try:
            pais_divisao, temporada = c[0], c[1]
            df = partidas_campeonato(pais_divisao, temporada)
            path_save = path('datalake')+f'/jogos_ids/{pais_divisao}/{temporada}.csv'
            df.to_csv(path_save, index=False)
            metadata['jogos_ids'][pais_divisao][temporada] = 'evaluation'
            with open(path('datalake')+'/metadata.json', 'w') as fp:
                json.dump(metadata, fp)
            logging.info(f"INFO etl.data_lake.partidas_campeonato.update_partidas_campeonato: "
                         f"Update league {pais_divisao} | {temporada}.")
        except Exception as err:
            logging.error("ERROR etl.data_lake.partidas_campeonato.update_partidas_campeonato: "
                          f"Could not update league {pais_divisao} | {temporada}")
            logging.error(err)
            return
        
    if len(campeonatos)==0:    
        logging.info("INFO etl.data_lake.partidas_campeonato.update_partidas_campeonato: "
                     "All leagues already up to date.")