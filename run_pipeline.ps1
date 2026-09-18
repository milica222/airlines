<#
.SYNOPSIS
    Runs the full airline pipeline in Docker end to end: builds/starts the Spark
    cluster, runs the ingest+transform+validate steps, then starts the notebook.

.PARAMETER Down
    Tear down all containers (docker compose down) instead of running the pipeline.

.PARAMETER SkipNotebook
    Run the pipeline but skip starting the Jupyter notebook service at the end.

.PARAMETER Workers
    Number of Spark worker containers to start (default 1). Each worker
    advertises 2 cores / 2G, so -Workers 2 gives the cluster 4 cores / 4G.
#>

param(
    [switch]$Down,
    [switch]$SkipNotebook,
    [int]$Workers = 1
)

$ErrorActionPreference = "Stop"

function Fail($message) {
    Write-Host $message -ForegroundColor Red
    exit 1
}

if ($Down) {
    Write-Host "Stopping containers..." -ForegroundColor Cyan
    docker compose down
    exit $LASTEXITCODE
}

Write-Host "Checking Docker engine..." -ForegroundColor Cyan
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Fail "Docker engine is not responding. Start/restart Docker Desktop, then re-run this script."
}

Write-Host "Building image and starting Spark cluster ($Workers worker(s))..." -ForegroundColor Cyan
docker compose up -d --build --scale spark-worker=$Workers spark-master spark-worker
if ($LASTEXITCODE -ne 0) { Fail "Failed to start spark-master/spark-worker." }

Write-Host "Running pipeline (download -> transform -> validate)..." -ForegroundColor Cyan
# --no-deps is required: without it, "compose run" resets linked services to
# their default scale of 1 and would tear down the extra workers started above.
docker compose run --rm --no-deps app python src/pipeline.py
if ($LASTEXITCODE -ne 0) { Fail "Pipeline run failed. Check the logs above." }

if (-not $SkipNotebook) {
    Write-Host "Starting notebook service..." -ForegroundColor Cyan
    docker compose up -d notebook
    if ($LASTEXITCODE -ne 0) { Fail "Failed to start notebook service." }
    Write-Host "Notebook available at http://localhost:8888" -ForegroundColor Green
}

Write-Host "Done. Results are in results/ and data/processed/flights_cleaned." -ForegroundColor Green
Write-Host "Run '.\run_pipeline.ps1 -Down' to stop all containers." -ForegroundColor Green
