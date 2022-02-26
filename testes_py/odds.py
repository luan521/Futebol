import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import json
from cafu.queries import GetOdds
from cafu.metadata import path
path_save = path('dir_results')

campeonato = 'franca'
def f():
    query = GetOdds()
    query.get_campeonato_dafabet(campeonato)
    
    query.join_link_odds_partida(0)
    query.open_odds()
    odds = query.get_odds()
    
    query.web.close() # encerra a sessão
    
    with open(path_save+'/odds.json', 'w') as fp:
        json.dump(odds, fp)
        
if __name__=='__main__':
    f()