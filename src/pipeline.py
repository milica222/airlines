import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def run_step(name: str, script: str) -> None:
    started = time.perf_counter()
    logging.info("[%s] %s", datetime.now().strftime("%Y-%m-%d %H:%M"), name)
    cmd = [sys.executable, str(SRC / script)]
    completed = subprocess.run(cmd, cwd=str(ROOT), check=False)
    duration = time.perf_counter() - started

    if completed.returncode != 0:
        raise RuntimeError(
            f"Step failed: {name} ({script}), exit_code={completed.returncode}, duration_sec={duration:.2f}"
        )

    logging.info(
        "[%s] Zavrseno: %s (trajanje %.2fs)",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        name,
        duration,
    )


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    total_started = time.perf_counter()

    run_step("Preuzimanje podataka...", "download.py")
    run_step("Transformacija pokrenuta...", "transform.py")
    run_step("Validacija rezultata...", "validate_outputs.py")
    total_duration = time.perf_counter() - total_started
    logging.info(
        "[%s] Rezultati upisani u results/ (ukupno %.2fs)",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        total_duration,
    )


if __name__ == "__main__":
    main()
