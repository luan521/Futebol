from tqdm import tqdm
from cafu.queries.partida import Partida
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'\\logs.log'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def dados_partida(id_, max_iterate=50):
    """
    Função auxiliar (id_left_right).
    Busca os dados da partida, entra em loop até que os dados sejam retornados
        
    Args:
        id_: (int) id da partida
        max_iterate: número máximo de tentativas
    Returns:
         list: campeonato, times, date 
    """
    
    stop = False
    count = 1
    with tqdm(total=max_iterate) as barra_progresso:
        while not stop and count<=max_iterate:
            try:
                req = Partida(str(id_))
                campeonato = req.campeonato()
                times = req.nomes_times()
                date = req.data()
                stop = True
            except:
                count+=1
            barra_progresso.update(1)
    
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
        
    try:
        if partidas is None:
            total = 100
        else:
            total = 380-len(partidas)
        with tqdm(total=total) as barra_progresso:
            while campeonato == campeonato_fix:
                id_ = id_ + fator
                campeonato, times, date = dados_partida(id_)
                partidas.append(times)
                dates.append(date)
                ids.append(id_)
                if len(set(partidas)) < len(partidas):
                    break
                barra_progresso.update(1)

        id_ = id_ - fator
        partidas = partidas[:-1]
        dates = dates[:-1]
        ids = ids[:-1]

        logging.info(f"SUCCESS utils.etl.partidas_campeonato.id_left_right: Function executed successfully. <id_inicial>={id_inicial}, <campeonato_fix>={campeonato_fix}, <left>={left}, len(<partidas>)={len(partidas)}")
            
        return ids, partidas, dates
    except Exception as err:
        logging.error("ERROR utils.etl.partidas_campeonato.id_left_right: Unexpected error: Could not execute function. <id_inicial>={id_inicial}, <campeonato_fix>={campeonato_fix}, <left>={left}, <partidas>={partidas}, <dates>={dates}, <ids>={ids}")
        logging.error(err)
            
        return