from pyspark.sql import SparkSession

def get_spark(memory, delta = False):
    """
    Cria uma sessão do spark e uma sessão do delta lake
    
    Args:
        memory: (int) valor da memória do driver e executor
        delta: (bool) flag para definir o uso do delta lake
    Returns:
        (spark session), (delta lake session, optional)
    """
    spark = (
        SparkSession
        .builder
        .config('spark.sql.broadcastTimeout', '360000')
        .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer')
        .config('spark.driver.memory', f'{memory}G')
        .config('spark.executor.memory', f'{memory}G')
        .config('spark.driver.maxResultSize', '4G')
        .config('spark.sql.debug.maxToStringFields', 100)
        .config('spark.ui.showConsoleProgress', 'true')
        .config("spark.databricks.delta.schema.autoMerge.enabled", "true")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.databricks.delta.retentionDurationCheck.enabled", "false")
        .config("spark.databricks.delta.vacuum.parallelDelete.enabled", "true")
        
        .getOrCreate()
    )
    
    spark.sparkContext.setLogLevel("ERROR")

    if delta:
        from delta.tables import DeltaTable
        return spark, DeltaTable

    return spark

def read_delta(spark, datapath, version=None, timestamp=None, filter_=None):
    """
    Ler dados em formato delta
    
    Args:
        spark: (spark session) spark session
        datapath: (str) caminho dos arquivos a serem lidos
        version: (int) versão que será lida do delta lake
        timestamp: (timestamp) timestamp da versão que será lida do delta lake
        filter_: (str) filtro que será aplicado antes de retornar o dataframe
    Returns:
        (spark dataframe)
    """
    
    if version is not None:
        response = spark.read.format("delta").option("versionAsOf", version).load(datapath)
    elif timestamp is not None:
        response = spark.read.format("delta").option("timestampAsOf", timestamp).load(datapath)
    else:
        response = spark.read.format("delta").load(datapath)
    
    if filter_ is not None:
        response = response.filter(filter_)
    
    return response

def save_delta(df, datapath):
    """
    Salva o data frame em formato delta
    
    Args:
        df: (spark dataframe) dataframe a ser salvo
        datapath: (str) caminho onde o dataframe será salvo
    """
    df.write.format("delta").mode('overwrite').save(datapath)
    
def restore_delta_to_version(spark, datapath, version=None, timestamp=None):
    """
    Restaura a versão do delta, ou para a version=<version> ou para timestamp=<timestamp>
    
    Args:
        spark: (spark session) spark session
        datapath: (str) caminho do dataframe em formato delta, que será atualizado
        version: (int) versão do delta que será restaurada
        timestamp: (timestamp) timestamp do delta que será restaurada
    """
    if version is not None:
        df_restore = spark.read.format("delta").option("versionAsOf", version).load(datapath)
    if timestamp is not None:
        df_restore = spark.read.format("delta").option("timestampAsOf", timestamp).load(datapath)
    save_delta(df_restore, datapath)
    
def update_historical_delta(spark, DeltaTable, path_historical_data, df_new, 
                            columns_unique_update_historical_delta, 
                            filter_update = None, columns_update = 'all'):
    """
    Atualiza os dados históricos, em formato delta
    
    Args:
        spark: (spark session) spark session
        DeltaTable: (DeltaTable) DeltaTable session
        path_historical_data: (str) caminho do dataframe em formato delta, que será atualizado
        df_new: (spark dataframe) dataframe novo, contendo os novos dados, em relação aos dados históricos
        columns_unique_update_historical_delta: (list) colunas chaves, cujos valores não se duplicam na tabela
        filter_update: (str) Filtro na linguagem SQL. Insere uma condição a mais para atualizar os dados, 
                       quando as colunas <columns_unique> do dataframe histórico, possuem os mesmos valores em <df_new>
        columns_update: (list) colunas que serão atualizadas quando as condições forem satisfeitas. 
                        <columns_update> = 'all': Todas as colunas serão atualizadas
    """
    df_table = DeltaTable.forPath(spark, path_historical_data)
    
    query_columns_unique = ""
    for c in columns_unique_update_historical_delta:
        query_columns_unique = query_columns_unique + f"oldData.{c} = newData.{c} and "
    query_columns_unique=query_columns_unique[:-5]
    
    if columns_update == 'all':
        (
            df_table
            .alias("oldData")
            .merge(df_new.alias("newData"),
                   query_columns_unique)
            .whenMatchedUpdateAll(filter_update)
            .whenNotMatchedInsertAll()
            .execute()
        )
    else:
        map_columns_update = {col: f"newData.{col}" for col in columns_update}
        (
            df_table
            .alias("oldData")
            .merge(df_new.alias("newData"),
                   query_columns_unique)
            .whenMatchedUpdate(filter_update, map_columns_update)
            .whenNotMatchedInsertAll()
            .execute()
        )
    df_table.vacuum()