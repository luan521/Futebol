import os
import json
from cafu.metadata.campeonatos_espn import campeonato_espn
from cafu.metadata.campeonatos_dafabet import campeonato_dafabet
from cafu.metadata.paths import path
path_datalake = path('datalake')

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def initialize_datalake():
    """
    Prepara o diretório do datalake
    
    ```
    ├── jogadores
    ├── jogos_ids
    ├── partidas
    ├── odds
    └── metadata.json
    ```
    """
    
    campeonatos = campeonato_espn()
    try:

        # criando diretórios
        os.mkdir(path_datalake+f'/jogos_ids')
        os.mkdir(path_datalake+f'/partidas')
        os.mkdir(path_datalake+f'/odds')
        os.mkdir(path_datalake+'/jogadores')
        campeonatos = list(campeonatos.keys())
        for c in campeonatos:
            os.mkdir(path_datalake+f'/jogos_ids/{c}')
            os.mkdir(path_datalake+f'/partidas/{c}')
        campeonatos = campeonato_dafabet()
        campeonatos = list(campeonatos.keys())
        campeonatos = set([c.split('-')[0] for c in campeonatos])
        for c in campeonatos:
            os.mkdir(path_datalake+f'/odds/{c}')
            
        # criando arquivo metadata
        metadata = {'jogos_ids':{c: {} for c in campeonatos}}
        with open(path_datalake+'/metadata.json', 'w') as fp:
            json.dump(metadata, fp)
        
        logging.info("SUCCESS utils.etl.datalake.initialize_datalake: Function executed successfully")
    except Exception as err:
        logging.error("ERROR utils.etl.datalake.initialize_datalake: "
                      "Could not execute function")
        logging.error(err)
        
def _check_evaluation_status_datalake():
    """
    Método interno da biblioteca.
    Checa se existem atualizações do data lake em estado de avaliação
    """
    
    path_metadata = path('datalake')+'/metadata.json'
    r = open(path_metadata, 'r')
    metadata = json.load(r)
    
    count_evaluation = 0
    
    # check jogos_ids
    for c in metadata['jogos_ids']:
        for t in metadata['jogos_ids'][c]:
            if metadata['jogos_ids'][c][t]=='evaluation':
                count_evaluation+=1
                
    if count_evaluation>0:
        logging.warning("WARNING utils.etl.datalake._check_evaluation_status_datalake: "
                        f"{count_evaluation} evaluation status on datalake")