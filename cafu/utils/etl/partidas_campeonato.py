from cafu.queries.partida import Partida

def dados_partida(id_):
    """
    Função auxiliar (id_left_right).
    Busca os dados da partida, entra em loop até que os dados sejam retornados
        
    Args:
        id_: (int) id da partida
    Returns:
         list: campeonato, times, date 
    """
    
    stop = False
    while not stop:
        try:
            req = Partida(str(id_))
            campeonato = req.campeonato()
            times = req.nomes_times()
            date = req.data()
            stop = True
        except:
            pass
    return campeonato, times, date

def id_left_right(id_inicial, campeonato_fix, left=True, partidas=None, dates=None, ids=None):
    """
    Percorre os ids dos jogos, iniciando por <id_inicial>, subtraindo quando <left> True, somando quando <left> False.
        
    Args:
        id_inicial: (int) id inicial 
        campeonato_fix: (str) campeonato, no formato fornecido pelo site da ESPN
        left: (bool) Se os jogos_ids serão percorridos para a esquerda ou direita, iniciando por <id_inicial>
        partidas: (list) elementos no formato (time_casa, time_visitante), utilizar quando estas partidas já tiverem sido computadas, optional
        dates: (list) datas das partidas já computadas, optional
        ids: (list) datas das partidas já computadas, optional
    Returns:
         list: ids, partidas, dates
    """
    
    if left:
        fator = -1
    else:
        fator = 1
    
    id_ = id_inicial 
    campeonato, times, date = dados_partida(id_)
    
    if partidas is None:
        partidas = [times]
    else:
        partidas.append(times)
    if dates is None:
        dates = [date]
    else:
        dates.append(date)
    if ids is None:
        ids = [id_]
    else:
        ids.append(id_)
        
    while campeonato == campeonato_fix:
        id_ = id_ + fator
        campeonato, times, date = dados_partida(id_)
        partidas.append(times)
        dates.append(date)
        ids.append(id_)
        if len(set(partidas)) < len(partidas):
            break
    
    id_ = id_ - fator
    partidas = partidas[:-1]
    dates = dates[:-1]
    ids = ids[:-1]
    
    return ids, partidas, dates