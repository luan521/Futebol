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

    if delta:
        from delta.tables import DeltaTable
        return spark, DeltaTable

    return spark