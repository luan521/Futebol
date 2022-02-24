campeonatos = {
               'brasil': {
                          '2020-2020': {
                                        'nome': '2020 Brasileiro Serie A',
                                        'id':  569982,
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