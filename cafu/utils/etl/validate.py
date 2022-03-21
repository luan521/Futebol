import json
import pandas as pd
import sys
from datetime import date
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
    
class ValidateExecution():
    """
    Análise da execução do código.
    <self.df_log>: (pandas dataframe) logs gerados no dia <day>.
    <self.important_functions>: (list) funções importantes para serem passadas como argumento 
    no método <self.print_description_error>
    
    Args:
        day: (str) dia da execução, format 'YYYY-mm-dd'
    """
    
    def __init__(self, day):
        
        self.important_functions = [
                                    'etl.data_lake.partidas_campeonato.partidas_campeonato',
                                    'utils.loop_try.loop_try'
                                   ]
        
        log_path = path('logs_cafu')+'/logs.txt'
        log_path = log_path[:29]+day+log_path[39:]
        with open(log_path) as f:
            lines = f.read().split('\n')
        columns = ['date', 'type', 'function', 'description1', 'description2']
        types = ['INFO', 'SUCCESS', 'P-1 SUCCESS','WARNING', 'ERROR']
        data = []
        for i in range(len(lines)):
            try:
                div = []
                j = 0
                while len(div)<=1:
                    div = lines[i].split(f' {types[j]} ')
                    j+=1
                date = div[0]
                type_ = types[j-1]
                function = div[1].split(': ')[0]
                description1 = div[1].split(function+': ')[1]
                data.append([date, type_, function, description1, []])
            except:
                data[-1][-1].append(lines[i])
        self.df_log = pd.DataFrame(data, columns=columns)
    
    def warning_types(self):
        """
        Filtra os warnings gerados e agrupa pela coluna functions. Resultado salvo em <self.df_warning>
        """
        
        index_filter = self.df_log['type'] == 'WARNING'
        self.df_warning = (
                              self.df_log[index_filter]
                              .groupby('function')['function']
                              .count()
                              .sort_values(ascending=False)
                          )
        
    def error_types(self):
        """
        Filtra os erros gerados e agrupa pela coluna functions. Resultado salvo em <self.df_error>
        """
        
        index_filter = self.df_log['type'] == 'ERROR'
        self.df_error = (
                            self.df_log[index_filter]
                            .groupby('function')['function']
                            .count()
                            .sort_values(ascending=False)
                        )
        
    def print_description_warning(self, function):
        """
        Printa o valor na coluna description1, para cada warning gerado na função <function>
        
        Args:
            function: (str) exemplos importantes em <self.important_functions>
        """
        
        index_filter = ((self.df_log['type'] == 'WARNING')&
                        (self.df_log['function']==function))
        for i in self.df_log[index_filter].index:
            print(self.df_log['description1'][i])
            print()
        
    def print_description_error(self, function):
        """
        Printa o valor na coluna description1, para cada erro gerado na função <function>
        
        Args:
            function: (str) exemplos importantes em <self.important_functions>
        """
        
        index_filter = ((self.df_log['type'] == 'ERROR')&
                        (self.df_log['function']==function))
        for i in self.df_log[index_filter].index:
            print(self.df_log['description1'][i])
            print()
            
def first_validation_execution():
    """
    Primeira validação da execução do código.
    
    Args:
        day: (str) dia da execução, format 'YYYY-mm-dd'
    Returns:
         dict: funções importantes que geraram erros - quantidade de erros gerados
    """
    
    today = str(date.today())
    help_ = f"""
            Primeira validação da execução do código.
    
            Args:
                day: (str) dia da execução, format 'YYYY-mm-dd'
                Ex (dia atual): {today}
            Returns:
                 dict: funções importantes que geraram erros - quantidade de erros gerados
             """
    
    args = sys.argv[1:]
    if len(args)==0:
        print(help_)
        return
    else:
        day = args[0]
        
    val = ValidateExecution(day)
    val.error_types()
    val.warning_types()
    response = {}
    response['error'] = {
                         f: val.df_error[f] for f in val.important_functions 
                                            if f in val.df_error
                        }
    response['warning'] = {
                           f: val.df_error[f] for f in val.important_functions 
                                            if f in val.df_warning
                          }
    return response