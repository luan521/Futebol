import os
path_project = os.path.abspath('..')
import sys
sys.path.append(path_project)

import pandas as pd
from cafu.queries import AtuacoesJogador, Bio
from cafu.metadata import path
path_save = path('dir_teste')

id_jogador = '252107/vinicius-junior'
def f():
    query = AtuacoesJogador(id_jogador)
    jogo = 1

    data = [
            query.campeonato(),
            query.date(jogo),
            query.casa_fora(jogo),
            query.adversario(jogo),
            query.resultado(jogo),
            query.gols(jogo),
            query.assistencias(jogo),
            query.finalizacoes(jogo),
            query.finalizacoes_no_gol(jogo),
            query.faltas_cometidas(jogo),
            query.faltas_sofridas(jogo),
            query.impedimentos(jogo),
            query.cartoes_amarelos(jogo),
            query.cartoes_vermelhos(jogo)
           ]
    
    query.web.close()
    
    index = [
             'campeonato',
             'date',
             'casa_fora',
             'adversario',
             'resultado',
             'gols',
             'assistencias',
             'finalizacoes',
             'finalizacoes_no_gol',
             'faltas_cometidas',
             'faltas_sofridas',
             'impedimentos',
             'cartoes_amarelos',
             'cartoes_vermelhos'
            ]
    
    df = pd.DataFrame(data=data, index=index)
    df.to_csv(path_save+'/atuacoes_jogador.csv')
    
    query = Bio(id_jogador)
    
    data = [
            query.time(1)[0],
            query.time(1)[1],
            query.posicao(),
            query.altura(),
            query.massa(),
            query.data_nascimento(),
            query.nacionalidade()
           ]

    query.web.close()

    index = [
             'time',
             'qt_temporadas',
             'posicao',
             'altura',
             'massa',
             'data_nascimento',
             'nacionalidade'
             ]
    
    df = pd.DataFrame(data=data, index=index)
    df.to_csv(path_save+'/bio_jogador.csv')
    
if __name__=='__main__':
    f()