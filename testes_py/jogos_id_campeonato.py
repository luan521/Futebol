import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import pandas as pd
from cafu.etl import partidas_campeonato
from cafu.metadata import path
path_save = path('dir_results')

pais_divisao, temporada = 'brasil', '2020-2020'
def f():
    df = partidas_campeonato(pais_divisao, temporada)
    
    df.to_csv(path_save+'/jogos_id_campeonato.csv', index=False)
    
if __name__=='__main__':
    f()