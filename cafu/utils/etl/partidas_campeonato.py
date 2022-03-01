from tqdm import tqdm
from cafu.queries.partida import Partida
from cafu.utils.loop_try import loop_try
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
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
    
    def _try_dados_partida():
        req = Partida(str(id_))
        campeonato = req.campeonato()
        times = req.nomes_times()
        date = req.date
        if (campeonato is not None) and (times is not None) and (date is not None):
            return True, [campeonato, times, date]
        else:
            return False, None
    success, response = loop_try(_try_dados_partida, max_iterate, time_sleep=1)
    
    if success:
        campeonato, times, date = response[0], response[1], response[2]
        return campeonato, times, date
    else:
        return

def id_left_right(id_inicial, campeonato_fix, qt_partidas_campeonato, left=True, partidas=None, dates=None, ids=None):
    """
    Percorre os ids dos jogos, iniciando por <id_inicial>, subtraindo quando <left> True, somando quando <left> False.
        
    Args:
        id_inicial: (int) id inicial 
        campeonato_fix: (str) campeonato, no formato fornecido pelo site da ESPN
        qt_partidas_campeonato: (int) quantidade total de partidas no campeonato
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
    
    try:
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
        
        if len(partidas)==1:
            total = qt_partidas_campeonato
        else:
            total = qt_partidas_campeonato-len(partidas)
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

        logging.info(f"SUCCESS utils.etl.partidas_campeonato.id_left_right: "
                     f"Function executed successfully. <id_inicial>={id_inicial}, "
                     f"<campeonato_fix>={campeonato_fix}, <left>={left}, len(<partidas>)={len(partidas)}")
            
        return ids, partidas, dates
    except Exception as err:
        logging.error("ERROR utils.etl.partidas_campeonato.id_left_right: Unexpected error: "
                      f"Could not execute function. <id_inicial>={id_inicial}, "
                      f"<campeonato_fix>={campeonato_fix}, <left>={left}, len(<partidas>)={len(partidas)}")
        logging.error(err)
            
        return