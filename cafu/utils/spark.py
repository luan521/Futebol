from pyspark.sql import SparkSession

def get_spark(memory):
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
        .getOrCreate()
    )
    
    spark.sparkContext.setLogLevel("ERROR")

    return spark