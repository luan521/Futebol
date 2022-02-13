import re
import time
from cafu.utils import WebdriverChrome
from cafu.utils.string import convert_str_var_time
from cafu.metadata.paths import path

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def find_id_jogadores(jogo_id):
    """
    Args:
        jogo_id: (int or str) completa o link https://www.espn.com.br/futebol/escalacoes?jogoId=<jogo_id>. 
    Returns:
        list: códigos dos jogadores que foram inscritos para a partida, referente ao <jogo_id>
    """
    
    init = time.time()
    
    try:
        web = WebdriverChrome()
        link_partida = f'https://www.espn.com.br/futebol/escalacoes?jogoId={str(jogo_id)}'
        web.web.get(link_partida)
        padrao = 'jogador/.+/id/[0-9]+/.+'
        links_0 = web.web.find_elements_by_tag_name('a')
        links = [l.get_attribute('href') for l in links_0]
        web.web.close()
        logging.info("P-1 SUCCESS etl.data_lake.jogadores_partida.find_id_jogadores: Links collected on match page")
    except:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.error(f"ERROR etl.data_lake.jogadores_partida.find_id_jogadores: "
                      f"Could not collect links on match page. <jogo_id>={jogo_id}. runtime = {runtime_str}")
        return
    
    ids_jogadores = []
    for l in links:
        try:
            id_ = re.findall(padrao, l)[0][13:]
            id_part1 = id_.split('/')[0]
            id_part2 = id_.split('/')[1]
            ids_jogadores.append({'id_part1': id_part1, 'id_part2': id_part2})
        except:
            pass
    
    if len(ids_jogadores) >= 22:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.info(f"SUCCESS etl.data_lake.jogadores_partida.find_id_jogadores: "
                     f"Function executed successfully. <jogo_id>={jogo_id}. runtime = {runtime_str}")
    else:
        end = time.time()
        runtime_str = convert_str_var_time(init, end)
        logging.error(f"ERROR etl.data_lake.jogadores_partida.find_id_jogadores: "
                      f"{len(ids_jogadores)} players were found. <jogo_id>={jogo_id}. runtime = {runtime_str}")
        return
    return ids_jogadores