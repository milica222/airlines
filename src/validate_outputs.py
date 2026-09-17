import argparse
from pathlib import Path

from spark_utils import create_spark_session


DEFAULT_CLEANED_PATH = Path("data/processed/flights_cleaned")
DEFAULT_RESULTS_PATH = Path("results")
REQUIRED_RESULTS_DATASETS = [
    "top_10_routes_avg_dep_delay",
    "cancelled_pct_by_airline_year",
    "monthly_arr_delay_rolling3",
    "delay_frequency_by_day_period",
    "delay_category_distribution",
]


def validate_cleaned(spark, cleaned_path: Path) -> None:
    if not cleaned_path.exists():
        raise FileNotFoundError(f"Cleaned dataset path does not exist: {cleaned_path}")

    df = spark.read.parquet(str(cleaned_path))
    count = df.count()
    if count == 0:
        raise ValueError("Cleaned dataset is empty.")

    required_columns = ["FlightDate", "DepDelay", "ArrDelay", "delay_category", "year", "month"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Cleaned dataset missing required columns: {missing}")

    print(f"Cleaned dataset validation passed. Rows: {count}")


def validate_results(spark, results_path: Path) -> None:
    if not results_path.exists():
        raise FileNotFoundError(f"Results path does not exist: {results_path}")

    for dataset_name in REQUIRED_RESULTS_DATASETS:
        dataset_path = results_path / dataset_name
        if not dataset_path.exists():
            raise FileNotFoundError(f"Missing required results dataset: {dataset_path}")

        df = spark.read.parquet(str(dataset_path))
        count = df.count()
        if count == 0:
            raise ValueError(f"Results dataset is empty: {dataset_path}")

        print(f"Results dataset validation passed: {dataset_name} (rows={count})")


def run(cleaned_path: Path, results_path: Path) -> None:
    spark = create_spark_session("validate-outputs")
    try:
        validate_cleaned(spark, cleaned_path)
        validate_results(spark, results_path)
        print("All output validations passed.")
    finally:
        spark.stop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate cleaned and results outputs")
    parser.add_argument("--cleaned-path", type=Path, default=DEFAULT_CLEANED_PATH)
    parser.add_argument("--results-path", type=Path, default=DEFAULT_RESULTS_PATH)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.cleaned_path, args.results_path)
