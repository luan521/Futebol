import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import pandas as pd
from cafu.etl import partidas_campeonato
from cafu.metadata import path
path_save = path('dir_results')

def f():
    help_ = (
             f"""
             Args:
                pais_divisao: (str) chave primária do dicionário campeonatos, caminho metadata/campeonatos_espn
                temporada: (str) chave secundária do dicionário campeonatos, caminho metadata/campeonatos_espn
             Ex: espanha 2021-2022
             Resultado salvo em: {path_save}/jogos_id_campeonato.csv
             """
            )
    
    args = sys.argv[1:]
    if len(args) == 0:
        print(help_)
    else:
        df = partidas_campeonato(*args)
        df.to_csv(path_save+'/jogos_id_campeonato.csv', index=False)
    
if __name__=='__main__':
    f()