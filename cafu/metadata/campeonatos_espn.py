campeonatos = {
               'brasil': {
                          '2021-2021': {
                                        'nome': '2021 Brasileiro Serie A',
                                        'id':  598234,
                                        'qt_jogos_rodada': 10
                                       },
                          '2020-2020': {
                                        'nome': '2020 Brasileiro Serie A',
                                        'id':  569982,
                                        'qt_jogos_rodada': 10
                                       },
                          '2019-2019': {
                                        'nome': '2019 Brasileirao',
                                        'id':  538252,
                                        'qt_jogos_rodada': 10
                                       },
                          '2018-2018': {
                                        'nome': 'Brasileirao 2018',
                                        'id':  507099,
                                        'qt_jogos_rodada': 10
                                       },
                          '2017-2017': {
                                        'nome': 'Brasileirao 2017',
                                        'id':  476167,
                                        'qt_jogos_rodada': 10
                                       },
                          '2016-2016': {
                                        'nome': 'Brasileirao 2016',
                                        'id':  446123,
                                        'qt_jogos_rodada': 10
                                       },
                          '2015-2015': {
                                        'nome': 'Brasileirao 2015',
                                        'id':  417601,
                                        'qt_jogos_rodada': 10
                                       },
                          '2014-2014': {
                                        'nome': 'Brasileirao 2014',
                                        'id':  390494,
                                        'qt_jogos_rodada': 10
                                       }
                         },
               'franca': {
                          '2021-2022': {
                                        'nome': '2021-22 Ligue 1',
                                        'id':  609280,
                                        'qt_jogos_rodada': 10
                                       },
                          '2020-2021': {
                                        'nome': '2020-21 Ligue 1',
                                        'id':  572924,
                                        'qt_jogos_rodada': 10
                                       },
                          '2019-2020': {
                                        'nome': 'Temporada regular',
                                        'id':  541893,
                                        'qt_jogos_rodada': 10
                                       }
                         },
               'espanha': {
                           '2021-2022': {
                                         'nome': '2021-22 LaLiga',
                                         'id': 610557,
                                         'qt_jogos_rodada': 10
                                        },
                           '2020-2021': {
                                         'nome': '2020-2021 LaLiga',
                                         'id': 582111,
                                         'qt_jogos_rodada': 10
                                        },
                           '2019-2020': {
                                         'nome': '2019-2020 LaLiga',
                                         'id': 550377,
                                         'qt_jogos_rodada': 10
                                        },
                           '2018-2019': {
                                         'nome': '2018-2019 Spanish Primera División',
                                         'id': 521904,
                                         'qt_jogos_rodada': 10
                                        },
                           '2017-2018': {
                                         'nome': '2017-2018 Spanish Primera División',
                                         'id': 490354,
                                         'qt_jogos_rodada': 10
                                        },
                           '2016-2017': {
                                         'nome': '2016/2017 Spanish Primera División',
                                         'id': 458740,
                                         'qt_jogos_rodada': 10
                                        },
                           '2015-2016': {
                                         'nome': 'Primeira Divisão Espanhola 2015/16',
                                         'id': 433618,
                                         'qt_jogos_rodada': 10
                                        },
                           '2014-2015': {
                                         'nome': 'Primeira Divisão Espanhola 2014/15',
                                         'id': 402285,
                                         'qt_jogos_rodada': 10
                                        },
                           '2013-2014': {
                                         'nome': '2013-2014 Spanish Primera División',
                                         'id': 372857,
                                         'qt_jogos_rodada': 10
                                        },
                           '2012-2013': {
                                         'nome': '2012/2013 Spanish Primera División',
                                         'id': 348204,
                                         'qt_jogos_rodada': 10
                                        },
                           '2011-2012': {
                                         'nome': 'Primeira Divisão Espanhola - 2011/12',
                                         'id': 323700,
                                         'qt_jogos_rodada': 10
                                        }
                          }
              }

def campeonato_espn(pais_divisao=None, temporada=None):
    """
    Args:
        pais_divisao: (str) chave primária do dicionário campeonatos
        temporada: (str) chave secundária do dicionário campeonatos
    Returns:
        dict: nome do campeonato no site ESPN, id de um jogo qualquer do campeonato, quantidade de jogos em uma rodada.
        Se nenhum argumento é definido, retorna <campeonatos>.
        Se apenas <pais_divisao> é definido, retorna a resposta para todas as temporadas definidas para <pais_divisao>
    """
    
    response =  campeonatos
    if pais_divisao is not None:
        response = response[pais_divisao]
    if temporada is not None:
        response = response[temporada]
    return response