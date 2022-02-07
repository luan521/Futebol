import pandas as pd
from cafu.utils.etl.partidas_campeonato import id_left_right
from cafu.metadata.campeonatos_espn import campeonato_espn
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def partidas_campeonato(pais_divisao, temporada, qt_jogos_rodada=10):
    """
    Busca as partidas do campeonato <campeonato_fix>
        
    Args:
        pais_divisao: (str) chave primária do dicionário campeonatos, caminho metadata/campeonatos_espn
        temporada: (str) chave secundária do dicionário campeonatos, caminho metadata/campeonatos_espn
        qt_jogos_rodada: (int) quantidade de jogos que ocorrem em uma rodada
    Returns:
         pandas dataframe: jogo_id, dates, rodada, time_casa, time_visitante
    """
    
    dados_campeonato = campeonato_espn(pais_divisao, temporada) 
    campeonato, id_inicial = dados_campeonato['nome'], dados_campeonato['id']
    ids, partidas, dates = id_left_right(id_inicial, campeonato)
    ids, partidas, dates = id_left_right(id_inicial+1, campeonato, left=False, partidas=partidas, dates=dates, ids=ids)
    
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
        
        logging.info(f"SUCCESS etl.data_lake.partidas_campeonato.partidas_campeonato: Function executed successfully. "
                     f"<pais_divisao>={pais_divisao}, <temporada>={temporada}, <qt_jogos_rodada>={qt_jogos_rodada}")
        return df
    except:
        logging.error(f"ERROR etl.data_lake.partidas_campeonato.partidas_campeonato: Unexpected error: "
                      f"Could not execute function. <pais_divisao>={pais_divisao}, <temporada>={temporada}, "
                      f"<qt_jogos_rodada>={qt_jogos_rodada}")
        logging.error(err)
        return