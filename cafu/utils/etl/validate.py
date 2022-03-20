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
    def _update_partidas():
        if len(args)<=1:
            for c in metadata['partidas']:
                for t in metadata['partidas'][c]:
                    for j in metadata['partidas'][c][t]:
                        if metadata['partidas'][c][t][j]['status']=='evaluation':
                            metadata['partidas'][c][t][j]['status']=success_failed
        elif len(args)==2:
            c = args[1]
            for t in metadata['partidas'][c]:
                for j in metadata['partidas'][c][t]:
                    if metadata['partidas'][c][t][j]['status']=='evaluation':
                        metadata['partidas'][c][t][j]['status']=success_failed
        elif len(args)==3:
            c = args[1]
            t = args[2]
            for j in metadata['partidas'][c][t]:
                if metadata['partidas'][c][t][j]['status']=='evaluation':
                    metadata['partidas'][c][t][j]['status']=success_failed
        elif len(args)==4:
            c = args[1]
            t = args[2]
            j = args[3]
            try:
                metadata['partidas'][c][t][j]['status']
                metadata['partidas'][c][t][j]['status']=success_failed
            except:
                logging.error(f"ERROR utils.etl.validate.{function}: "
                              f"{c}.{t}.{j} doesn't exist in metadata['partidas']")
    def _update_jogadores():
        if len(args)<=1:
            for c in metadata['jogadores']:
                for t in metadata['jogadores'][c]:
                    for j in metadata['jogadores'][c][t]:
                        if metadata['jogadores'][c][t][j]=='evaluation':
                            metadata['jogadores'][c][t][j]=success_failed
        elif len(args)==2:
            c = args[1]
            for t in metadata['jogadores'][c]:
                for j in metadata['jogadores'][c][t]:
                    if metadata['jogadores'][c][t][j]=='evaluation':
                        metadata['jogadores'][c][t][j]=success_failed
        elif len(args)==3:
            c = args[1]
            t = args[2]
            for j in metadata['jogadores'][c][t]:
                if metadata['jogadores'][c][t][j]=='evaluation':
                    metadata['jogadores'][c][t][j]=success_failed
        elif len(args)==4:
            c = args[1]
            t = args[2]
            j = args[3]
            try:
                metadata['jogadores'][c][t][j]
                metadata['jogadores'][c][t][j]=success_failed
            except:
                logging.error(f"ERROR utils.etl.validate.{function}: "
                              f"{c}.{t}.{j} doesn't exist in metadata['jogadores']")
        
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
                 Chaves do dicionário datalake/metadata.json, que serão verificadas 
             """

    try:
        if len(args)==0:
            print(help_)
        elif args[0]=='jogos_ids':
            _update_jogos_ids()
        elif args[0]=='partidas':
            _update_partidas()
        elif args[0]=='jogadores':
            _update_jogadores()
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
        strs: chaves do dicionário datalake/metadata.json, que serão verificadas 
    """
    
    args = sys.argv[1:]
    _validate_invalidate_datalake('success', args)
    
   
        
def invalidate_datalake():
    """
    Invalida as atualizações no arquivo datalake/metadata.json. Quando todas as chaves
    do dicionário são passadas, a atualização sempre ocorre, caso contrário a atualização
    ocorre apenas no status "evaluation"
        
    Args:
        strs: chaves do dicionário datalake/metadata.json, que serão verificadas 
    """
    
    args = sys.argv[1:]
    _validate_invalidate_datalake('failed', args)