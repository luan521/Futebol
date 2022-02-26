import os
import json
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
    
    try:
        # criando arquivo metadata
        metadata = {}
        with open(path_datalake+'/metadata.json', 'w') as fp:
            json.dump(metadata, fp)

        # criando diretórios
        os.mkdir(path_datalake+'/jogadores')
        os.mkdir(path_datalake+'/jogos_ids')
        os.mkdir(path_datalake+'/odds')
        os.mkdir(path_datalake+'/partidas')
        
        logging.info("SUCCESS utils.etl.datalake.initialize_datalake: Function executed successfully")
    except Exception as err:
        logging.error("ERROR utils.etl.datalake.initialize_datalake: Unexpected error: "
                      "Could not execute function")
        logging.error(err)