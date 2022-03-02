import pandas as pd
from cafu.utils.string import identify_string_in_list
from cafu.utils.etl.datalake import _check_evaluation_status_datalake
from cafu.metadata.paths import path
path_jogos_ids = path('datalake')+'/jogos_ids'

def find_jogo_id(time_casa0, time_visitante0, campeonato, temporada):
    """
    Encontra o id da partida <time_casa0> vs <time_visitante0>, 
    em datalake/jogos_ids/<campeonato>/<temporada>.csv
         
    Args:
        time_casa0: (str) time da casa
        time_visitante0: (str) time visitante
        campeonato: (str) chave primária do dicionário campeonatos, caminho metadata/campeonatos_espn
        temporada: (str) chave secundária do dicionário campeonatos, caminho metadata/campeonatos_espn
    Returns:
         int: id da partida no site ESPN
    """
    
    _check_evaluation_status_datalake()
    
    try:
        df = pd.read_csv(f'{path_jogos_ids}/{campeonato}/{temporada}.csv')
        times = list(df['time_casa'].drop_duplicates())
    except Exception as err:
        logging.error("ERROR utils.queries.find_jogo_id.find_jogo_id: "
                      "Could not import csv file")
        logging.error(err)
        return
    
    index = identify_string_in_list(time_casa0, times)
    time_casa = times[index]
    index = identify_string_in_list(time_visitante0, times)
    time_visitante = times[index]
    
    index_filter = (
                    (df['time_casa']==time_casa)&
                    (df['time_visitante']==time_visitante)
                   )
    response = df[index_filter]['jogo_id'].item()
    
    return response