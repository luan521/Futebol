import pandas as pd
from datetime import datetime
from cafu.metadata.campeonatos_espn import campeonato_espn
from cafu.metadata import get_schema
from cafu.metadata.paths import path
path_datalake = path('datalake')

import logging
filename = path('logs_cafu')+'/logs.txt'
logging.basicConfig(filename=filename, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.INFO)

def _count_null_values(df):
    """
    Método interno da biblioteca cafu.
    Conta a quantidade de valores nulos no dataframe <df>, com exceção da coluna date_update
    """
    
    df.cache()
    count = df.count()
    count_null_values = {}
    for c in df.columns:
        if c != 'date_update':
            count_null = (
                             df
                             .filter(f'{c} is NULL')
                             .count()
                         )
            count_null_values[c] = count_null/count
    count_null_values['date_update'] = datetime.now()
    response = pd.DataFrame([count_null_values])
    return response

def update_null_values(spark, info):
    """
    Atualiza a quantidade de valores nulos nos dataframes de <info>, em datalake/evolution_null_values
    
    Args:
        spark: (spark session) 
        info: (str) partidas or jogadores
    """
    
    if info == 'jogadores':
        path_df = path('datalake')+'/jogadores/df_jogadores'
        df_jogadores = spark.read.parquet(path_df)
        df_null_values = _count_null_values(df_jogadores)
        (
            df_null_values
            .to_csv(
                    path('datalake')
                    +'/evolution_null_values/jogadores/df_jogadores.csv',
                    mode='a', header=False
                   )
        )
    elif info == 'partidas':
        campeonatos = campeonato_espn()
        for c in campeonatos:
            df_resumo = spark.read.parquet(path('datalake')+f'/partidas/resumo/{c}/df_resumo')
            df_jogadores = spark.read.parquet(path('datalake')+f'/partidas/jogadores_minutagens/{c}/df_jogadores')
            df_gols = spark.read.parquet(path('datalake')+f'/partidas/gols/{c}/df_gols')
            df_minuto_a_minuto = spark.read.parquet(path('datalake')+f'/partidas/descricoes/{c}/df_minuto_a_minuto')
            df_null_values = _count_null_values(df_resumo)
            (
                df_null_values
                .to_csv(
                        path('datalake')
                        +f'/evolution_null_values/partidas/resumo/{c}/df_resumo.csv',
                        mode='a', header=False
                       )
            )
            df_null_values = _count_null_values(df_jogadores)
            (
                df_null_values
                .to_csv(
                        path('datalake')
                        +f'/evolution_null_values/partidas/jogadores_minutagens/{c}/df_jogadores.csv',
                        mode='a', header=False
                       )
            )
            df_null_values = _count_null_values(df_gols)
            (
                df_null_values
                .to_csv(
                        path('datalake')
                        +f'/partidas/gols/{c}/df_gols',
                        mode='a', header=False
                       )
            )
            df_null_values = _count_null_values(df_minuto_a_minuto)
            (
                df_null_values
                .to_csv(
                        path('datalake')
                        +f'/partidas/descricoes/{c}/df_minuto_a_minuto.csv',
                        mode='a', header=False
                       )
            )
        else:
            logging.error("ERROR etl.datalake.null_values.update_null_values: "
                          "Arg <info> must be or 'partidas' or 'jogadores'")