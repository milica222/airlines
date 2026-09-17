import os
from pyspark.sql import SparkSession


def create_spark_session(app_name: str) -> SparkSession:
    """Create a SparkSession with explicit runtime settings from env vars."""
    # The driver (this container) runs as root, but Spark workers run as a
    # separate non-root user, so directories the driver creates must be
    # world-writable or workers get permission-denied writing into them.
    os.umask(0)
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
