import json
import sys
from cafu.metadata.paths import path
path_metadata = path('datalake')+'/metadata.json'

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def validate_datalake():
    """
    Valida as atualizações no arquivo datalake/metadata.json, com status evaluation
        
    Args:
        option1: Chaves do dicionário datalake/metadata.json, que serão validadas 
        option2: Quando nenhum argumento é passado, todas as atualizações são validadas
    """
    
    args = sys.argv[1:]
    
    def _update_jogos_ids():
        if len(args)<=1:
            for c in metadata['jogos_ids']:
                for t in metadata['jogos_ids'][c]:
                    metadata['jogos_ids'][c][t]='success'
        elif len(args)==2:
            c = args[1]
            for t in metadata['jogos_ids'][c]:
                metadata['jogos_ids'][c][t]='success'
        elif len(args)==3:
            c = args[1]
            t = args[2]
            metadata['jogos_ids'][c][t]='success'
    
    def _update_all():
        _update_jogos_ids()
            
    try:
        r = open(path_metadata, 'r')
        metadata = json.load(r)
    except Exception as err:
        logging.error("ERROR utils.etl.validate.validate_datalake: "
                      "Could not import datalake/metadata.json")
        logging.error(err)
        return

    try:
        if len(args)==0:
            _update_all()
        elif args[0]=='jogos_ids':
            _update_jogos_ids()
    except Exception as err:
        logging.error("ERROR utils.etl.validate.validate_datalake: "
                      f"Could not update metadata. <args>={args}")
        logging.error(err)
        return
        
    with open(path_metadata, 'w') as fp:
        json.dump(metadata, fp)