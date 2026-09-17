import argparse
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from spark_utils import create_spark_session


DEFAULT_RAW_PATH = Path("data/raw/T_ONTIME_REPORTING.csv")
DEFAULT_CLEANED_PATH = Path("data/processed/flights_cleaned")
DEFAULT_RESULTS_PATH = Path("results")

REQUIRED_COLUMNS = [
    "FlightDate",
    "Reporting_Airline",
    "Origin",
    "Dest",
    "DepDelay",
    "ArrDelay",
    "Cancelled",
    "CancellationCode",
]

COLUMN_ALIASES = {
    "FlightDate": ["FlightDate", "FL_DATE"],
    "Reporting_Airline": ["Reporting_Airline", "OP_UNIQUE_CARRIER"],
    "Origin": ["Origin", "ORIGIN"],
    "Dest": ["Dest", "DEST"],
    "DepDelay": ["DepDelay", "DEP_DELAY"],
    "ArrDelay": ["ArrDelay", "ARR_DELAY"],
    "Cancelled": ["Cancelled", "CANCELLED"],
    "CancellationCode": ["CancellationCode", "CANCELLATION_CODE"],
    "CRSDepTime": ["CRSDepTime", "CRS_DEP_TIME"],
    "DepTime": ["DepTime", "DEP_TIME"],
}


def normalize_input_schema(df: DataFrame) -> DataFrame:
    normalized = df
    upper_to_actual = {name.upper(): name for name in df.columns}

    for canonical_name, aliases in COLUMN_ALIASES.items():
        if canonical_name in normalized.columns:
            continue

        source_column = None
        for alias in aliases:
            actual = upper_to_actual.get(alias.upper())
            if actual:
                source_column = actual
                break

        if source_column:
            normalized = normalized.withColumn(canonical_name, F.col(source_column))

    return normalized


def validate_required_columns(df: DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Input CSV missing required columns: {missing}")


def classify_delay_category(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "delay_category",
        F.when(F.col("DepDelay") <= 0, F.lit("no_delay"))
        .when((F.col("DepDelay") >= 1) & (F.col("DepDelay") <= 15), F.lit("small"))
        .when((F.col("DepDelay") >= 16) & (F.col("DepDelay") <= 60), F.lit("medium"))
        .otherwise(F.lit("large")),
    )


def add_date_partitions(df: DataFrame) -> DataFrame:
    parsed_date = F.coalesce(
        F.to_date(F.col("FlightDate"), "M/d/yyyy h:mm:ss a"),
        F.to_date(F.col("FlightDate")),
    )
    return (
        df.withColumn("FlightDate", parsed_date)
        .withColumn("year", F.year("FlightDate"))
        .withColumn("month", F.month("FlightDate"))
    )


def add_departure_hour(df: DataFrame) -> DataFrame:
    # Prefer scheduled departure time; fallback to actual departure time.
    dep_time_source = F.coalesce(F.col("CRSDepTime"), F.col("DepTime"))
    padded_time = F.lpad(F.col("_dep_time_int").cast("string"), 4, "0")

    return (
        df.withColumn("_dep_time_int", dep_time_source.cast("int"))
        .withColumn(
            "departure_hour",
            F.when(
                F.col("_dep_time_int").isNotNull(),
                F.substring(padded_time, 1, 2).cast("int"),
            ),
        )
        .drop("_dep_time_int")
    )


def add_day_period(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "day_period",
        F.when((F.col("departure_hour") >= 6) & (F.col("departure_hour") < 12), F.lit("jutro"))
        .when((F.col("departure_hour") >= 12) & (F.col("departure_hour") < 18), F.lit("popodne"))
        .when((F.col("departure_hour") >= 18) & (F.col("departure_hour") < 24), F.lit("vece"))
        .otherwise(F.lit("noc")),
    )


def compute_and_write_results(df: DataFrame, results_path: Path) -> None:
    results_path.mkdir(parents=True, exist_ok=True)
    df.createOrReplaceTempView("flights_cleaned")

    top_routes = df.sparkSession.sql(
        """
        SELECT
            Origin,
            Dest,
            ROUND(AVG(DepDelay), 2) AS avg_dep_delay,
            COUNT(*) AS flights_count
        FROM flights_cleaned
        GROUP BY Origin, Dest
        ORDER BY avg_dep_delay DESC, flights_count DESC
        LIMIT 10
        """
    )
    top_routes.write.mode("overwrite").parquet(str(results_path / "top_10_routes_avg_dep_delay"))

    cancelled_pct = df.sparkSession.sql(
        """
        WITH carrier_year AS (
            SELECT
                year,
                Reporting_Airline,
                100.0 * SUM(CASE WHEN Cancelled = 1 THEN 1 ELSE 0 END) / COUNT(*) AS cancelled_pct
            FROM flights_cleaned
            GROUP BY year, Reporting_Airline
        ),
        ranked AS (
            SELECT
                year,
                Reporting_Airline,
                ROUND(cancelled_pct, 4) AS cancelled_pct,
                ROW_NUMBER() OVER (PARTITION BY year ORDER BY cancelled_pct DESC, Reporting_Airline ASC) AS rn
            FROM carrier_year
        )
        SELECT year, Reporting_Airline, cancelled_pct
        FROM ranked
        WHERE rn = 1
        ORDER BY year
        """
    )
    cancelled_pct.write.mode("overwrite").parquet(str(results_path / "cancelled_pct_by_airline_year"))

    monthly_delay = df.sparkSession.sql(
        """
        WITH monthly_base AS (
            SELECT
                year,
                month,
                ROUND(AVG(ArrDelay), 2) AS avg_arr_delay
            FROM flights_cleaned
            GROUP BY year, month
        ),
        monthly_with_index AS (
            SELECT
                year,
                month,
                avg_arr_delay,
                year * 100 + month AS ym_index
            FROM monthly_base
        )
        SELECT
            year,
            month,
            avg_arr_delay,
            ROUND(
                AVG(avg_arr_delay) OVER (
                    ORDER BY ym_index
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ),
                2
            ) AS rolling_3m_avg_arr_delay
        FROM monthly_with_index
        ORDER BY year, month
        """
    )
    monthly_delay.write.mode("overwrite").parquet(str(results_path / "monthly_arr_delay_rolling3"))

    day_period = df.sparkSession.sql(
        """
        SELECT
            day_period,
            COUNT(*) AS total_flights,
            SUM(CASE WHEN DepDelay > 0 THEN 1 ELSE 0 END) AS delayed_flights,
            ROUND(100.0 * SUM(CASE WHEN DepDelay > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS delayed_pct
        FROM flights_cleaned
        GROUP BY day_period
        ORDER BY delayed_pct DESC, delayed_flights DESC
        """
    )
    day_period.write.mode("overwrite").parquet(str(results_path / "delay_frequency_by_day_period"))

    delay_category_distribution = df.sparkSession.sql(
        """
        SELECT
            delay_category,
            COUNT(*) AS flights_count,
            ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
        FROM flights_cleaned
        GROUP BY delay_category
        ORDER BY flights_count DESC
        """
    )
    delay_category_distribution.write.mode("overwrite").parquet(
        str(results_path / "delay_category_distribution")
    )


def run(raw_path: Path, cleaned_path: Path, results_path: Path) -> None:
    spark = create_spark_session("airline-transform")
    try:
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw CSV not found at {raw_path}")

        df = spark.read.option("header", True).option("inferSchema", True).csv(str(raw_path))
        df = normalize_input_schema(df)
        validate_required_columns(df)

        df = df.withColumn("DepDelay", F.col("DepDelay").cast("double"))
        df = df.withColumn("ArrDelay", F.col("ArrDelay").cast("double"))
        df = df.withColumn("Cancelled", F.col("Cancelled").cast("int"))

        cleaned_df = df.filter(F.col("DepDelay").isNotNull() & F.col("ArrDelay").isNotNull())
        cleaned_df = classify_delay_category(cleaned_df)
        cleaned_df = add_date_partitions(cleaned_df)
        cleaned_df = add_departure_hour(cleaned_df)
        cleaned_df = add_day_period(cleaned_df)

        cleaned_df.coalesce(1).write.mode("overwrite").partitionBy("year", "month").parquet(str(cleaned_path))

        compute_and_write_results(cleaned_df, results_path)
        print(f"Cleaned parquet saved to: {cleaned_path}")
        print(f"Results saved to: {results_path}")
    finally:
        spark.stop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transform airline CSV and compute SQL analytics")
    parser.add_argument("--raw-path", type=Path, default=DEFAULT_RAW_PATH)
    parser.add_argument("--cleaned-path", type=Path, default=DEFAULT_CLEANED_PATH)
    parser.add_argument("--results-path", type=Path, default=DEFAULT_RESULTS_PATH)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.raw_path, args.cleaned_path, args.results_path)
