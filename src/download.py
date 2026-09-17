import argparse
import hashlib
import csv
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import requests


DEFAULT_SOURCE = Path("data/T_ONTIME_REPORTING.csv")
DEFAULT_RAW_DIR = Path("data/raw")
DEFAULT_RAW_NAME = "T_ONTIME_REPORTING.csv"
DEFAULT_METADATA_NAME = "download_metadata.json"
DEFAULT_METADATA_HISTORY_NAME = "download_metadata_history.jsonl"
DEFAULT_TIMEOUT_SECONDS = 120


def sha256_of_file(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def count_rows_best_effort(file_path: Path) -> int | None:
    try:
        with file_path.open("r", encoding="utf-8", newline="") as f:
            return max(sum(1 for _ in f) - 1, 0)
    except Exception:
        return None


def validate_csv_file(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"Expected CSV file does not exist: {file_path}")
    if file_path.stat().st_size == 0:
        raise ValueError(f"CSV file is empty: {file_path}")

    with file_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
    if not header:
        raise ValueError(f"CSV file has no header: {file_path}")
    return header


def download_from_url(url: str, destination: Path, timeout_seconds: int) -> None:
    response = requests.get(url, timeout=timeout_seconds)
    response.raise_for_status()
    destination.write_bytes(response.content)


def timestamp_suffix() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_raw_target_path(raw_dir: Path, write_mode: str) -> Path:
    if write_mode == "overwrite":
        return raw_dir / DEFAULT_RAW_NAME

    snapshots_dir = raw_dir / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    stem, ext = os.path.splitext(DEFAULT_RAW_NAME)
    return snapshots_dir / f"{stem}_{timestamp_suffix()}{ext}"


def append_metadata_history(history_path: Path, metadata: dict) -> None:
    with history_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(metadata, ensure_ascii=True) + "\n")


def run(
    source_path: Path,
    raw_dir: Path,
    source_url: str | None,
    write_mode: str,
    timeout_seconds: int,
) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = build_raw_target_path(raw_dir, write_mode)

    if source_url:
        download_from_url(source_url, raw_path, timeout_seconds)
        source_descriptor = source_url
        source_kind = "url"
    else:
        if not source_path.exists():
            raise FileNotFoundError(
                f"Source dataset not found at {source_path}. Provide --url or place raw CSV in data/."
            )
        shutil.copy2(source_path, raw_path)
        source_descriptor = f"local://{source_path.as_posix()}"
        source_kind = "local"

    header = validate_csv_file(raw_path)

    latest_path = raw_dir / DEFAULT_RAW_NAME
    if raw_path != latest_path:
        shutil.copy2(raw_path, latest_path)

    metadata = {
        "source": source_descriptor,
        "source_type": source_kind,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_file_name": raw_path.name,
        "raw_file_path": str(raw_path.as_posix()),
        "latest_file_name": latest_path.name,
        "raw_sha256": sha256_of_file(raw_path),
        "raw_size_bytes": raw_path.stat().st_size,
        "write_mode": write_mode,
        "row_count_best_effort": count_rows_best_effort(raw_path),
        "column_count": len(header),
        "columns": header,
    }

    metadata_path = raw_dir / DEFAULT_METADATA_NAME
    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=True, indent=2)
    history_path = raw_dir / DEFAULT_METADATA_HISTORY_NAME
    append_metadata_history(history_path, metadata)

    print(f"Raw CSV saved to: {raw_path}")
    print(f"Raw latest pointer saved to: {latest_path}")
    print(f"Raw metadata saved to: {metadata_path}")
    print(f"Raw metadata history appended to: {history_path}")
    return raw_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download/copy airline CSV dataset to data/raw")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument(
        "--write-mode",
        type=str,
        choices=["overwrite", "snapshot"],
        default="snapshot",
    )
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(
        source_path=args.source,
        raw_dir=args.raw_dir,
        source_url=args.url,
        write_mode=args.write_mode,
        timeout_seconds=args.timeout_seconds,
    )
