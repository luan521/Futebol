from pyspark.sql.types import (StructType, StructField, 
                               StringType, DateType, IntegerType, FloatType)
from cafu.metadata.paths import path
path_datalake = path('datalake')

schema_datalake = {
                   'partidas_resumo': StructType([ 
                                        StructField("campeonato",StringType(),True), 
                                        StructField("campeonato_metadata",StringType(),True), 
                                        StructField("temporada_metadata",StringType(),True), 
                                        StructField("date",DateType(),True), 
                                        StructField("formacao_time_casa",StringType(),True), 
                                        StructField("formacao_time_visitante", StringType(), True), 
                                        StructField("jogo_id", IntegerType(), True), 
                                        StructField("rodada", IntegerType(), True),
                                        StructField("time_casa", StringType(), True), 
                                        StructField("time_casa_cartoes_amarelos", IntegerType(), True),
                                        StructField("time_casa_cartoes_vermelhos", IntegerType(), True), 
                                        StructField("time_casa_chutes_fora", IntegerType(), True), 
                                        StructField("time_casa_chutes_nogol", IntegerType(), True), 
                                        StructField("time_casa_defesas", IntegerType(), True), 
                                        StructField("time_casa_escanteios", IntegerType(), True), 
                                        StructField("time_casa_faltas_cometidas", IntegerType(), True),
                                        StructField("time_casa_gols_feitos", IntegerType(), True),
                                        StructField("time_casa_impedimentos", IntegerType(), True),
                                        StructField("time_casa_posse", FloatType(), True),
                                        StructField("time_visitante", StringType(), True), 
                                        StructField("time_visitante_cartoes_amarelos", IntegerType(), True),
                                        StructField("time_visitante_cartoes_vermelhos", IntegerType(), True),
                                        StructField("time_visitante_chutes_fora", IntegerType(), True),
                                        StructField("time_visitante_chutes_nogol", IntegerType(), True),
                                        StructField("time_visitante_defesas", IntegerType(), True),
                                        StructField("time_visitante_escanteios", IntegerType(), True),
                                        StructField("time_visitante_faltas_cometidas", IntegerType(), True),
                                        StructField("time_visitante_gols_feitos", IntegerType(), True),
                                        StructField("time_visitante_impedimentos", IntegerType(), True),
                                        StructField("time_visitante_posse", FloatType(), True)
                                      ]),
                   'partidas_jogadores_minutagens': StructType([ 
                                                        StructField("camisa", IntegerType(), True),
                                                        StructField("final_jogando", IntegerType(), True),
                                                        StructField("inicio_jogando", IntegerType(), True),
                                                        StructField("nome", StringType(), True),
                                                        StructField("casa_visitante", StringType(), True),
                                                        StructField("jogo_id", IntegerType(), True)
                                                      ])
                  }

f"""
Local paths of databases in <schema_datalake>:

- partidas_resumo: {path_datalake}/partidas/resumo

- partidas_descricoes: {path_datalake}/partidas/descricoes

- partidas_gols: {path_datalake}/partidas/gols

- partidas_jogadores_minutagens: {path_datalake}/partidas/jogadores_minutagens
"""

def get_schema(database):
    """
    Args:
        database: (str) chave do dicionário schema_datalake
    Returns:
        StructType: schema da base de dados <database> no data lake
    """
    
    return schema_datalake[database]