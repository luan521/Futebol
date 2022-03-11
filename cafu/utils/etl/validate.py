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

def _validate_invalidate_datalake(success_failed, args):
    """
    Método interno da biblioteca cafu.
    Valida ou invalida as atualizações no arquivo datalake/metadata.json. 
        
    Args:
        success_failed: (bool) success or failed
        args: (list)
    """
    
    def _update_jogos_ids():
        if len(args)<=1:
            for c in metadata['jogos_ids']:
                for t in metadata['jogos_ids'][c]:
                    if metadata['jogos_ids'][c][t]=='evaluation':
                        metadata['jogos_ids'][c][t]=success_failed
        elif len(args)==2:
            c = args[1]
            for t in metadata['jogos_ids'][c]:
                if metadata['jogos_ids'][c][t]=='evaluation':
                    metadata['jogos_ids'][c][t]=success_failed
        elif len(args)==3:
            c = args[1]
            t = args[2]
            try:
                metadata['jogos_ids'][c][t]
                metadata['jogos_ids'][c][t]=success_failed
            except:
                logging.error(f"ERROR utils.etl.validate.{function}: "
                              f"{c}.{t} doesn't exist in metadata['jogos_ids']")
        
    if success_failed=='success':
        function = 'validate_datalake'
        complement_help = 'Valida'
    elif success_failed=='failed':
        function = 'invalidate_datalake'
        complement_help = 'Invalida'
            
    try:
        r = open(path_metadata, 'r')
        metadata = json.load(r)
    except Exception as err:
        logging.error(f"ERROR utils.etl.validate.{function}: "
                      "Could not import datalake/metadata.json")
        logging.error(err)
        return
    
    help_ = f"""
             {complement_help} as atualizações no arquivo datalake/metadata.json. Quando todas as chaves
             do dicionário são passadas, a atualização sempre ocorre, caso contrário a atualização
             ocorre apenas no status "evaluation"

             Args:
                 option1: Chaves do dicionário datalake/metadata.json, que serão verificadas 
                 option2: Quando nenhum argumento é passado, todas as atualizações são verificadas
             """

    try:
        if len(args)==0:
            print(help_)
        elif args[0]=='jogos_ids':
            _update_jogos_ids()
    except Exception as err:
        logging.error(f"ERROR utils.etl.validate.{function}: "
                      f"Could not update metadata. <args>={args}")
        logging.error(err)
        return
        
    try:
        with open(path_metadata, 'w') as fp:
            json.dump(metadata, fp)
    except Exception as err:
        logging.error(f"ERROR utils.etl.validate.{function}: "
                      f"Could not save metadata. <args>={args}")
        logging.error(err)
        return

def validate_datalake():
    """
    Valida as atualizações no arquivo datalake/metadata.json. Quando todas as chaves
    do dicionário são passadas, a validação sempre ocorre, caso contrário a atualização
    ocorre apenas no status "evaluation"
        
    Args:
        option1: Chaves do dicionário datalake/metadata.json, que serão verificadas 
        option2: Quando nenhum argumento é passado, todas as atualizações são verificadas
    """
    
    args = sys.argv[1:]
    _validate_invalidate_datalake('success', args)
    
   
        
def invalidate_datalake():
    """
    Invalida as atualizações no arquivo datalake/metadata.json. Quando todas as chaves
    do dicionário são passadas, a atualização sempre ocorre, caso contrário a atualização
    ocorre apenas no status "evaluation"
        
    Args:
        option1: Chaves do dicionário datalake/metadata.json, que serão verificadas 
        option2: Quando nenhum argumento é passado, todas as atualizações são verificadas
    """
    
    args = sys.argv[1:]
    _validate_invalidate_datalake('failed', args)