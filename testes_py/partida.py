import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import pandas as pd
from cafu.queries import Partida
from cafu.metadata import path
path_save = path('dir_results')


jogo_id = '614698'
def f():
    
    req = Partida(jogo_id)
    
    data = [
            req.teste_jogo_finalizado(),
            req.campeonato(),
            req.data(),
            req.nomes_times(),
            req.formacao(),
            req.jogadores(),
            req.gols(),
            req.placar(),
            req.posse(),
            req.chutes_fora_nogol(),
            req.faltas(),
            req.cartoes_amarelos(),
            req.cartoes_vermelhos(),
            req.impedimentos(),
            req.escanteios(),
            req.defesas()
           ]
    index = [
             'teste_jogo_finalizado',
             'campeonato',
             'data',
             'nomes_times',
             'formacao',
             'jogadores',
             'gols',
             'placar',
             'posse',
             'chutes_fora_nogol',
             'faltas',
             'cartoes_amarelos',
             'cartoes_vermelhos',
             'impedimentos',
             'escanteios',
             'defesas'
            ]
    df = pd.DataFrame(data=data, index=index)
    df.to_csv(path_save+'/partida.csv')
    
    minuto_a_minuto = req.minuto_a_minuto()
    df = pd.DataFrame(minuto_a_minuto)
    df.to_csv(path_save+'/descricao_partida.csv', index=False)
    
if __name__=='__main__':
    f()