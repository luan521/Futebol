import os
import pandas as pd
import json
from datetime import date
from cafu.utils.spark_delta import get_spark
from cafu.metadata.schema_datalake import get_schema
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
        os.mkdir(path_datalake+f'/partidas/resumo')
        os.mkdir(path_datalake+f'/partidas/descricoes')
        os.mkdir(path_datalake+f'/partidas/gols')
        os.mkdir(path_datalake+f'/partidas/jogadores_minutagens')
        os.mkdir(path_datalake+f'/partidas/partidas_canceladas')
        os.mkdir(path_datalake+f'/odds')
        os.mkdir(path_datalake+'/jogadores')
        campeonatos = list(campeonatos.keys())
        for c in campeonatos:
            os.mkdir(path_datalake+f'/jogos_ids/{c}')
            os.mkdir(path_datalake+f'/partidas/resumo/{c}')
            os.mkdir(path_datalake+f'/partidas/descricoes/{c}')
            os.mkdir(path_datalake+f'/partidas/gols/{c}')
            os.mkdir(path_datalake+f'/partidas/jogadores_minutagens/{c}')
        campeonatos = campeonato_dafabet()
        campeonatos = list(campeonatos.keys())
        campeonatos = set([c.split('-')[0] for c in campeonatos])
        for c in campeonatos:
            os.mkdir(path_datalake+f'/odds/{c}')
            
        # criando spark dataframes bases
        campeonatos = campeonato_espn()
        spark = get_spark(1)
        schema = get_schema('partidas_resumo')
        df_resumo = spark.createDataFrame(data=[], schema=schema)
        schema = get_schema('partidas_jogadores_minutagens')
        df_jogadores = spark.createDataFrame(data=[], schema=schema)
        schema = get_schema('partidas_gols')
        df_gols = spark.createDataFrame(data=[], schema=schema)
        schema = get_schema('partidas_descricoes')
        df_minuto_a_minuto = spark.createDataFrame(data=[], schema=schema)
        for c in campeonatos:
            df_resumo.write.parquet(path_datalake+
                                    f'/partidas/resumo/{c}/df_resumo')
            df_jogadores.write.parquet(path_datalake+
                                       f'/partidas/jogadores_minutagens/{c}/df_jogadores')
            df_gols.write.parquet(path_datalake+
                                  f'/partidas/gols/{c}/df_gols')
            df_minuto_a_minuto.write.parquet(path_datalake+
                                             f'/partidas/descricoes/{c}/df_minuto_a_minuto')
        schema = get_schema('partidas_canceladas')
        df_partidas_canceladas = spark.createDataFrame(data=[], schema=schema)
        df_partidas_canceladas.write.parquet(path_datalake+'/partidas/partidas_canceladas/df_canceladas')
            
        # criando arquivo metadata
        campeonatos = campeonato_espn()
        metadata = {'jogos_ids':{c: {} for c in campeonatos}, 
                    'partidas': {c: {} for c in campeonatos}}
        with open(path_datalake+'/metadata.json', 'w') as fp:
            json.dump(metadata, fp)
        
        logging.info("SUCCESS utils.etl.datalake.initialize_datalake: Function executed successfully")
    except Exception as err:
        logging.error("ERROR utils.etl.datalake.initialize_datalake: "
                      "Could not execute function")
        logging.error(err)
        
def proximas_partidas():
    """
    Análisa datalake.jogos_ids, e retorna as datas das próximas partidas dos campeonatos em aberto,
    ou se o campeonato já foi finalizado
        
    Returns:
        dict: campeonato, temporada - se já foi finalizado ou data da próxima partida
    """
    
    today = date.today()
    
    r = open(path_datalake+'/metadata.json', 'r')
    metadata_datalake = json.load(r)
    
    campeonatos = [
                   [k1, k2] for k1 in list(metadata_datalake['jogos_ids'].keys()) 
                            for k2 in list(metadata_datalake['jogos_ids'][k1].keys())
                            if metadata_datalake['jogos_ids'][k1][k2] != 'failed'
                  ]
    
    response = {c:{} for c in metadata_datalake['jogos_ids']}
    for c in campeonatos:
        df = pd.read_csv(path_datalake+f'/jogos_ids/{c[0]}/{c[1]}.csv')
        if len(df[df['dates']>=str(today)]['dates'])==0:
            response[c[0]][c[1]] = 'finalizado'
        else:
            response[c[0]][c[1]] = min(df[df['dates']>=str(today)]['dates'])
    
    return response

def partidas_desatualizadas():
    """
    Análisa datalake.jogos_ids e datalake.metadata, e retorna os jogos desatualizados em 
    datalake.partidas, datalake.descricoes_partidas
        
    Returns:
        dict: campeonato, temporada - lista de jogos desatualizados
    """
    
    today = date.today()

    r = open(path_datalake+'/metadata.json', 'r')
    metadata_datalake = json.load(r)

    campeonatos = [
                   [k1, k2] for k1 in list(metadata_datalake['jogos_ids'].keys()) 
                            for k2 in list(metadata_datalake['jogos_ids'][k1].keys())
                            if metadata_datalake['jogos_ids'][k1][k2] != 'failed'
                  ]

    jogos_desatualizados = {}
    for c in campeonatos:
        df = pd.read_csv(path_datalake+f'/jogos_ids/{c[0]}/{c[1]}.csv')
        jogos_ocorridos = df[df['dates']<str(today)]['jogo_id']
        jogos_atualizados = []
        try:
            for j in metadata_datalake['partidas'][c[0]][c[1]]:
                if metadata_datalake['partidas'][c[0]][c[1]][str(j)]['status'] != 'failed':
                    jogos_atualizados.append(int(j))
        except:
            pass

        jogos_desatualizados_c =  list(set(jogos_ocorridos).difference(jogos_atualizados))
        if len(jogos_desatualizados_c)>0:
            try:
                jogos_desatualizados[c[0]][c[1]] = jogos_desatualizados_c
            except:
                jogos_desatualizados[c[0]] = {}
                jogos_desatualizados[c[0]][c[1]] = jogos_desatualizados_c
                
    return jogos_desatualizados
        
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