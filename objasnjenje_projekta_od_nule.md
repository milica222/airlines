# Objasnjenje projekta od nule: Analiza kasnjenja letova

Ovaj dokument je napravljen za nekoga ko krece od nule.
Cilj je da razumes:
1. sta projekat radi,
2. zasto je svaka faza potrebna,
3. sta je uradjeno u kodu,
4. cemu sluze fajlovi,
5. kako da mislis o podacima i rezultatima.

## 1. Sta je zapravo zadatak

Imamo jedan veliki CSV sa podacima o letovima:
- data/T_ONTIME_REPORTING.csv

Iz tog CSV-a treba da napravimo automatski data pipeline koji:
1. pripremi podatke,
2. ocisti lose redove,
3. izracuna analiticke metrike,
4. sacuva rezultate u efikasnom formatu,
5. omoguci vizualizaciju i CI automatizaciju.

To znaci da ne radimo posao rucno svaki put, nego jednom napises proces i posle ga samo pokrenes.

## 2. Najvazniji pojmovi (jednostavno)

### 2.1 CSV

CSV je obican tekstualni fajl sa kolonama i redovima.
Dobar je za razmenu podataka, ali nije idealan za brzu analitiku nad velikim podacima.

### 2.2 Parquet

Parquet je format fajla za analitiku nad velikim podacima.

Zasto je Parquet bitan:
1. Kolonarni je format: cita samo kolone koje ti trebaju.
2. Kompresovan je: zauzima manje prostora.
3. Brzi je za Spark SQL upite.
4. Dobar je za data lake i BI/analitiku.

Zato je logika ovde:
1. Ulaz je CSV (raw format sa interneta/dataset-a).
2. Obradjeni i analiticki izlazi su Parquet (brze i jeftinije citanje).

### 2.3 Spark

Spark je engine za obradu velikih podataka.
Radi paralelno i zato je dobar za velike CSV fajlove.

### 2.4 Pipeline

Pipeline znaci lanac koraka koji ide istim redom svaki put:
1. ingest,
2. transform,
3. analiza,
4. validacija.

## 3. Zasto sve ide kroz Docker

Sve je namerno organizovano da radi u Docker okruzenju.

Zasto:
1. Isti uslovi na svakom racunaru.
2. Manje problema sa verzijama biblioteka.
3. Lakse pokretanje Spark master/worker servisa.
4. Lakse pokretanje u GitHub Actions (isto okruzenje kao lokalno).

Drugim recima: Docker smanjuje "kod mene radi, kod tebe ne radi" problem.

## 4. Sta je uradjeno u ovom projektu

Projekat je migriran na novu temu (airline kasnjenja), i uradjene su sledece stvari:

1. Uklonjena je stara parking logika i stari izlazi.
2. Uveden je novi tok za airline CSV.
3. Dodata je schema normalizacija za BTS kolone (npr. FL_DATE -> FlightDate).
4. Transformacije su uskladjene sa zahtevom zadatka.
5. Spark SQL upiti kreiraju trazene rezultate.
6. Notebook je prebacen da cita rezultate iz results foldera.
7. CI workflow je podesen da pokrece pipeline i uploaduje artifact.
8. Sve je vraceno na Docker-first nacin rada.

## 5. Struktura fajlova i cemu sluze

### 5.1 Glavni ulaz

- data/T_ONTIME_REPORTING.csv
  - Pocetni dataset sa letovima.

### 5.2 Ingest

- src/download.py
  - Uzimanje lokalnog CSV-a i kopiranje u data/raw.
  - Upis metadata:
    - data/raw/download_metadata.json
    - data/raw/download_metadata_history.jsonl

Zasto ovaj korak postoji:
1. Da imas kontrolisan raw ulaz.
2. Da imas trag kada je podatak preuzet i koji je fajl koriscen.

### 5.3 Transform + SQL

- src/transform.py
  - Ucitava CSV,
  - proverava kolone,
  - odbacuje redove gde su DepDelay/ArrDelay null,
  - pravi delay_category,
  - dodaje year i month,
  - upisuje cleaned parquet,
  - izvrsava Spark SQL upite i upisuje rezultate u results.

Zasto ovaj korak postoji:
1. Da podaci budu kvalitetni i konzistentni.
2. Da analitika bude reproducibilna.

### 5.4 Validacija

- src/validate_outputs.py
  - Proverava da cleaned dataset i svi results dataseti postoje i nisu prazni.

Zasto ovaj korak postoji:
1. Da odmah uhvatis gresku ako je neki output izostao.
2. Da pipeline ne "prodje zeleno" sa losim izlazom.

### 5.5 Orkestracija

- src/pipeline.py
  - Pokrece sve redom:
    1. download,
    2. transform,
    3. validate.

Zasto ovaj korak postoji:
1. Jedna komanda pokrece ceo tok.
2. Lakse za automatizaciju i CI.

### 5.6 Spark konfiguracija

- src/spark_utils.py
  - Pravi SparkSession i podesava particije, memoriju, UI port.

Zasto ovaj korak postoji:
1. Centralizovana konfiguracija.
2. Lakse menjanje performansi bez editovanja vise fajlova.

### 5.7 Vizualizacija

- notebooks/analiza.ipynb
  - Ucitava results parquet i pravi trazene grafike.

Zasto ovaj korak postoji:
1. Da rezultat bude razumljiv i vizuelan.
2. Da mozes brzo da interpretiras nalaze.

### 5.8 CI

- .github/workflows/pipeline.yml
  - Manual trigger,
  - Docker build,
  - pipeline run,
  - upload results kao artifact.

Zasto ovaj korak postoji:
1. Automatizovano pokretanje.
2. Rezultati su dostupni za preuzimanje iz CI.

## 6. Sta tacno radi transformacija

U src/transform.py glavna logika je:

1. Ucitavanje CSV-a iz data/raw/T_ONTIME_REPORTING.csv.
2. Normalizacija imena kolona.
   - Primer:
     - FL_DATE postaje FlightDate,
     - DEP_DELAY postaje DepDelay,
     - OP_UNIQUE_CARRIER postaje Reporting_Airline.
3. Cast tipova za brojcane kolone.
4. Filter redova gde su kasnjenja null.
5. Dodavanje delay_category:
   - no_delay: DepDelay <= 0
   - small: 1-15
   - medium: 16-60
   - large: > 60
6. Dodavanje year i month iz datuma.
7. Dodavanje day_period (jutro/popodne/vece/noc) na osnovu sata poletanja.
8. Upis cleaned dataset-a u data/processed/flights_cleaned (partition by year, month).

## 7. Koji rezultati se generisu

U results se prave Parquet dataseti:

1. top_10_routes_avg_dep_delay
   - Top 10 ruta sa najvecim prosecnim kasnjenjem pri polasku.

2. cancelled_pct_by_airline_year
   - Po godini, prevoznik sa najvecim procentom otkazanih letova.

3. monthly_arr_delay_rolling3
   - Mesecni trend kasnjenja sa rolling prosekom od 3 meseca.

4. delay_frequency_by_day_period
   - Koliko su kasnjenja cesta po delu dana.

5. delay_category_distribution
   - Raspodela kasnjenja po kategorijama (za pie chart).

## 8. Zasto se radi particionisanje po year i month

Particionisanje znaci da Spark ne mora da cita sve podatke svaki put.
Ako te zanima samo jedan period, cita samo relevantne foldere.

To donosi:
1. brze upite,
2. manje I/O,
3. bolje skaliranje za vece datasete.

## 9. Kako izgleda pokretanje od pocetka do kraja (Docker)

1. Start Spark servisa:
- docker compose up -d --build spark-master spark-worker

2. Ingest lokalnog CSV:
- docker compose run --rm app python src/download.py --source data/T_ONTIME_REPORTING.csv --write-mode overwrite

3. Transform i SQL:
- docker compose run --rm app python src/transform.py

4. Validacija:
- docker compose run --rm app python src/validate_outputs.py

5. Sve odjednom:
- docker compose run --rm app python src/pipeline.py

6. Notebook:
- docker compose up -d notebook

7. Gasenje:
- docker compose down

## 10. Kako da znas da je sve dobro proslo

Proveri da postoje:
1. data/processed/flights_cleaned
2. results/top_10_routes_avg_dep_delay
3. results/cancelled_pct_by_airline_year
4. results/monthly_arr_delay_rolling3
5. results/delay_frequency_by_day_period
6. results/delay_category_distribution

Ako ovi folderi postoje i nisu prazni, pipeline je odradio posao.

## 11. Ceste greske i zasto se desavaju

1. Missing required columns
- Desava se kada header u CSV ne odgovara ocekivanim imenima.
- Reseno je alias mapiranjem u transform.py.

2. Prazan output
- Obicno znaci da je filter previse strog ili ulaz nema validne redove.
- Zato postoji validate_outputs.py.

3. Spark/Docker servis nije podignut
- app korak ne moze da se izvrsi bez master/worker servisa.

## 12. Jednostavna mentalna slika

Ako treba da zapamtis samo 3 stvari:
1. CSV je ulaz (sirov, sporiji za analitiku).
2. Parquet je izlaz (brz i efikasan za analizu).
3. Pipeline automatizuje ceo proces da bude ponovljiv i pouzdan.

---

Ako zelis, sledeci korak moze da bude jos jedan "mini" fajl od 1 strane sa skracenim cheat sheet-om (samo komande + sta proveravas posle svake komande).
