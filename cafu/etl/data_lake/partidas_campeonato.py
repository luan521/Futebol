import pandas as pd
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