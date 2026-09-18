import os
from pyspark.sql import SparkSession


def create_spark_session(app_name: str) -> SparkSession:
    """Create a SparkSession with explicit runtime settings from env vars."""
    # The driver (this container) runs as root. The spark-master/spark-worker
    # containers are pinned to user: root in docker-compose.yml to match, so
    # executors can write into the output directories the driver creates on the
    # shared bind mount. Without that, the apache/spark image runs as uid 185
    # and every write fails with "Mkdirs failed to create ...".
    # os.umask() alone does not fix it: Spark creates output directories via
    # Hadoop's FileSystem API, which applies its own fs.permissions.umask-mode
    # (default 022 -> mode 0755) and ignores the process umask.
    master = os.getenv("SPARK_MASTER", "local[*]")
    shuffle_partitions = os.getenv("SPARK_SQL_SHUFFLE_PARTITIONS", "8")
    executor_memory = os.getenv("SPARK_EXECUTOR_MEMORY", "2g")
    ui_port = os.getenv("SPARK_UI_PORT", "4040")

    spark = (
        SparkSession.builder.appName(app_name)
        .master(master)
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
        .config("spark.executor.memory", executor_memory)
        .config("spark.ui.port", ui_port)
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark
