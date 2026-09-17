# Analiza kasnjenja letova

Automatizovani PySpark data pipeline za obradu i analizu javno dostupnih podataka o kasnjenjima letova.

Primarni ulazni dataset u ovom projektu je:
- data/T_ONTIME_REPORTING.csv

## 1. Cilj projekta

Cilj je da se CSV podaci o letovima automatski obrade kroz sledece faze:
1. ingest novih CSV fajlova u raw zonu,
2. ciscenje i priprema podataka,
3. Spark SQL analitika,
4. cuvanje rezultata kao Parquet,
5. vizualizacija rezultata u notebook-u.

## 2. Struktura projekta

projekat/

- data/
  - raw/                     # raw CSV i metadata ingest-a
  - T_ONTIME_REPORTING.csv   # polazni dataset
- notebooks/
  - analiza.ipynb            # vizualizacija nad results/
- src/
  - download.py              # ingest CSV u data/raw
  - transform.py             # transformacije + Spark SQL upiti
  - pipeline.py              # orkestracija koraka
  - validate_outputs.py      # validacija intermediate i final izlaza
  - spark_utils.py           # SparkSession konfiguracija
- results/
  - ... parquet dataseti iz SQL upita
- .github/
  - workflows/
    - pipeline.yml           # ručno pokretanje pipeline-a i artifact upload
- README.md

## 3. Tehnologije

1. Python
2. PySpark
3. Jupyter Notebook
4. Parquet
5. GitHub Actions
6. Docker i Docker Compose (primarni nacin pokretanja)

## 4. Faze pipeline-a

### 4.1 Ingest

Skripta src/download.py:
1. Ucitava lokalni CSV ili skida CSV sa URL-a.
2. Validira da CSV postoji, nije prazan i ima header.
3. Upisuje fajl u data/raw kao latest ili snapshot.
4. Upisuje metadata fajlove:
   - data/raw/download_metadata.json
   - data/raw/download_metadata_history.jsonl

Podrzani argumenti:
- --source (podrazumevano data/T_ONTIME_REPORTING.csv)
- --url
- --write-mode (overwrite ili snapshot)
- --raw-dir (podrazumevano data/raw)

### 4.2 Transformacija i priprema

Skripta src/transform.py:
1. Ucitava CSV iz data/raw/T_ONTIME_REPORTING.csv.
2. Proverava obavezne kolone:
   - FlightDate, Reporting_Airline, Origin, Dest,
   - DepDelay, ArrDelay, Cancelled, CancellationCode
3. Odbacuje redove gde su DepDelay ili ArrDelay null.
4. Dodaje delay_category:
   - no_delay: DepDelay <= 0
   - small: 1-15
   - medium: 16-60
   - large: > 60
5. Dodaje year i month iz FlightDate.
6. Cisceni skup cuva kao Parquet particionisan po year i month u:
   - data/processed/flights_cleaned

### 4.3 Spark SQL analitika

transform.py registruje view flights_cleaned i kreira sledece rezultate u results/:
1. top_10_routes_avg_dep_delay
   - top 10 ruta Origin -> Dest po prosecnom kasnjenju polaska.
2. cancelled_pct_by_airline_year
   - prevoznik sa najvecim procentom otkazanih letova po godini.
3. monthly_arr_delay_rolling3
   - mesecni trend sa rolling prosekom kasnjenja dolaska od 3 meseca.
4. delay_frequency_by_day_period
   - ucestalost kasnjenja po delu dana (jutro/popodne/vece/noc).
5. delay_category_distribution
   - distribucija delay_category (za pie chart u notebook-u).

### 4.4 Validacija izlaza

Skripta src/validate_outputs.py proverava:
1. da data/processed/flights_cleaned postoji i nije prazan,
2. da sadrzi obavezne izvedene kolone,
3. da svi required datasets u results/ postoje i nisu prazni.

### 4.5 Orkestracija

Skripta src/pipeline.py pokrece korake redom:
1. Preuzimanje podataka...
2. Transformacija pokrenuta...
3. Validacija rezultata...
4. Rezultati upisani u results/

Logovi koriste trazeni timestamp format:
[YYYY-MM-DD HH:MM] poruka

## 5. Pokretanje projekta

### Docker-first (kao original)

Preduslovi:
1. Docker Desktop sa Docker Compose podrskom.
2. Slobodni portovi: 7077, 8080, 8081 i 8888.

### Jednim komandom (automatski)

Skripta `run_pipeline.ps1` u root-u projekta radi sve korake iz sekcije ispod odjednom:
build image, podizanje Spark servisa, `pipeline.py` (ingest + transformacija + validacija) i
podizanje notebook servisa.

```powershell
.\run_pipeline.ps1
```

Opcije:
- `.\run_pipeline.ps1 -SkipNotebook` — bez podizanja notebook servisa.
- `.\run_pipeline.ps1 -Down` — gasi sve kontejnere (isto sto i korak 7 ispod).

Skripta prvo proverava da li je Docker engine dostupan (`docker info`) i prekida sa jasnom
porukom ako nije, umesto da komande visualno "ne rade nista".

### Rucno, korak po korak

Pokretanje svega redom sa lokalnim CSV fajlom `data/T_ONTIME_REPORTING.csv`:

1. Build image i podizanje Spark servisa:

   ```bash
   docker compose up -d --build spark-master spark-worker
   ```

2. Ingest lokalnog CSV-a u `data/raw/`:

   ```bash
   docker compose run --rm app python src/download.py --source data/T_ONTIME_REPORTING.csv --write-mode overwrite
   ```

3. Transformacija i SQL rezultati:

   ```bash
   docker compose run --rm app python src/transform.py
   ```

4. Validacija izlaza:

   ```bash
   docker compose run --rm app python src/validate_outputs.py
   ```

5. Jednokomandno pokretanje celog toka (alternativa koracima 2-4):

   ```bash
   docker compose run --rm app python src/pipeline.py
   ```

6. Pokretanje notebook servisa:

   ```bash
   docker compose up -d notebook
   ```

7. Gasenje servisa:

   ```bash
   docker compose down
   ```

Posle pokretanja proveri da postoje folderi:
1. `data/processed/flights_cleaned`
2. `results/top_10_routes_avg_dep_delay`
3. `results/cancelled_pct_by_airline_year`
4. `results/monthly_arr_delay_rolling3`
5. `results/delay_frequency_by_day_period`
6. `results/delay_category_distribution`

### Lokalno pokretanje (bez Dockera)

Preduslovi:
1. Python 3.10+.
2. JDK 11 ili 17 instaliran lokalno (PySpark zahteva Javu; nije Python paket pa venv ne pokriva ovo).

Kreiranje virtuelnog okruzenja i instalacija zavisnosti:

```powershell
cd c:\Users\Milica\Desktop\airlines
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.lock.txt
```

Pokretanje koraka (bez `SPARK_MASTER` env varijable, Spark radi u `local[*]` rezimu):

```powershell
python src/download.py --source data/T_ONTIME_REPORTING.csv --write-mode overwrite
python src/transform.py
python src/validate_outputs.py
```

ili jednokomandno:

```powershell
python src/pipeline.py
```

## 6. Vizualizacija

Notebook notebooks/analiza.ipynb ucitava Parquet rezultate iz results/ i prikazuje:
1. Bar chart: top 10 ruta po kasnjenju,
2. Line chart: rolling average kasnjenja kroz mesece,
3. Pie chart: distribucija delay_category,
4. Tabelu: prevoznici sortirani po procentu otkazivanja.

## 7. GitHub Actions

Workflow .github/workflows/pipeline.yml:
1. pokretanje: workflow_dispatch,
2. build image,
3. pokretanje pipeline.py,
4. upload results/ kao GitHub Actions artifact (airline-results).

## 8. Napomene

1. Za deo dana koristi se sat poletanja iz CRSDepTime, a fallback je DepTime.
2. Ako ulazni CSV nema obavezne kolone, pipeline prekida sa jasnom greskom.
3. Ako je dataset veliki, preporuceno je podesiti Spark env varijable za particije i memoriju.
