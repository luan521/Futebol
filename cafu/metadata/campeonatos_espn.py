campeonatos = {
               'espanha': {
                           '2021-2022': {
                                         'nome': '2021-22 LaLiga',
                                         'id': 610557
                                        },
                           '2020-2021': {
                                         'nome': '2020-2021 LaLiga',
                                         'id': 582111
                                        },
                           '2019-2020': {
                                         'nome': '2019-2020 LaLiga',
                                         'id': 550377
                                        },
                           '2018-2019': {
                                         'nome': '2018-2019 Spanish Primera División',
                                         'id': 521904
                                        },
                          }
              }

def campeonato_espn(pais_divisao, temporada):
    """
    Args:
        pais_divisao: (str) chave primária do dicionário campeonatos
        temporada: (str) chave secundária do dicionário campeonatos
    Returns:
        dict: nome do campeonato no site ESPN, id de um jogo qualquer do campeonato
    """
    
    return campeonatos[pais_divisao][temporada]
    
    