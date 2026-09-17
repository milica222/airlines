# Plan implementacije: Mini Data Lake - Swiss Parking

## 1. Plan v1 (detaljan implementacioni plan)

1. Analiza izvornog JSON skupa i mapiranje seme
2. Dizajn Data Lake strukture po slojevima
3. Implementacija Bronze ingest koraka
4. Implementacija Silver transformacija i validacija
5. Implementacija Gold agregacija
6. Orkestracija pipeline toka sa logovanjem
7. Notebook analiza i vizuelizacije
8. CI automatizacija i commit rezultata
9. Dokumentacija i reproducibilnost

---

## 2. Detaljne faze

### Faza 1: Analiza i sema

1. Ucitati uzorak iz data/bike-and-car-parking.json
2. Utvrditi:
- jedinstveni identifikator parkinga
- kolone za kapacitet automobila i bicikala
- kolone za koordinate, grad, pristup invalidima, tip parkinga
3. Napraviti mapu standardizacije naziva kolona i mapu normalizacije tipa parkinga

### Faza 2: Data Lake struktura

1. Formirati bronze/silver/gold direktorijume i pravila upisa
2. Definisati naming konvenciju za izlazne dataset-e
3. Definisati metadata fajl za Bronze preuzimanje:
- source_url
- downloaded_at_utc
- raw_file_name
- raw_sha256
- row_count_best_effort

### Faza 3: Bronze

1. Downloader koji:
- preuzima sa API-ja ili direct link-a
- cuva neizmenjen JSON u lake/bronze
- upisuje metadata zapis
2. Idempotentnost:
- opcioni overwrite ili timestamped snapshot
3. Osnovna validacija:
- fajl postoji
- nije prazan
- parsiranje prolazi

### Faza 4: Silver

1. Ucitavanje Bronze JSON-a u Spark DataFrame
2. Standardizacija kolona:
- snake_case
- konzistentni tipovi podataka
3. Ciscenje:
- deduplikacija po parking ID
- validacija koordinata i filtriranje redova van granica Svajcarske
4. Normalizacija tipa parkinga na:
- garage
- open
- park_and_ride
- bike
5. Dodavanje canton:
- prvo na osnovu postojecih atributa (ako postoje)
- fallback preko koordinata i kantonalnog grida/poligona
6. Upis u lake/silver kao Parquet, particionisan po canton

### Faza 5: Gold

1. Registracija Silver sloja kao SQL view
2. Kreiranje i upis 4 agregata:
- gold/kapacitet_po_kantonu
- gold/tip_parkinga_po_gradu
- gold/dostupnost_za_invalide
- gold/park_and_ride
3. Upis svakog agregata u zaseban Parquet izlaz

### Faza 6: Orkestracija

1. Glavni pipeline pokrece Bronze -> Silver -> Gold
2. Jedinstveno logovanje:
- start/end po koraku
- trajanje
- broj ulaznih/izlaznih slogova
3. Exit kod razlicit od nule na fail

### Faza 7: Notebook

1. Ucitavanje Gold sloja
2. Vizualizacije:
- Bar chart: ukupan kapacitet po kantonu (auti vs bicikli)
- Mapa Svajcarske: lokacije parkinga obojene po tipu
- Bar chart: procenat parkinga sa pristupom invalidima po kantonu
- Tabela: top 10 gradova po broju Park & Ride kapaciteta
3. Notebook mora raditi iz istog Docker okruzenja kao pipeline

### Faza 8: CI automatizacija

1. workflow_dispatch trigger
2. Build + run pipeline
3. Commit Gold rezultata nazad u repozitorijum

### Faza 9: Dokumentacija

1. Azurirati README.md sa:
- opisom projekta
- uputstvom za pokretanje lokalno i kroz Docker
- opisom Bronze/Silver/Gold faza
- troubleshooting sekcijom

---

## 3. Revizija plana (sta menjamo pre implementacije)

1. Dodati strogu verzionu kontrolu zavisnosti zbog Spark/Python kompatibilnosti.
2. Definisati jedan runtime put:
- lokalno pokretanje kroz Docker container
- CI pokretanje kroz isti Docker image
3. Uvesti acceptance kriterijume po fazama:
- Bronze: fajl + metadata obavezno
- Silver: partition po canton i validne koordinate
- Gold: sva 4 izlaza postoje i nisu prazna
4. Dodati data quality checks:
- null procenat za kljucne kolone
- broj odbacenih redova po razlogu
5. Dodati fallback strategiju za canton mapiranje ako geospatial biblioteke nisu dostupne.
6. Dodati Make ciljeve ili task komande za brzo pokretanje.

---

## 4. Optimizovani zahtevi: sve kroz Docker (Spark, notebook, pipeline)

1. Jedan Docker image sa:
- Python
- PySpark
- JupyterLab
- bibliotekama za analizu i mapu
2. Jedan docker-compose sa servisima:
- spark-master
- spark-worker
- app (pipeline runner)
- notebook (Jupyter)
3. Volumeni:
- mapiranje data i lake direktorijuma na host radi trajnosti podataka
4. Mreza i portovi:
- Spark UI exposed port
- Jupyter exposed port
5. Standardne komande:
- build image
- run pipeline
- open notebook
6. CI koristi isti image i isti entrypoint kao lokalno okruzenje.
7. Dokumentacija favorizuje Docker-only pokretanje radi 100% reproduktivnosti.

---

## 5. Preporuceni redosled implementacije

1. Dockerfile + docker-compose + dependency lock
2. Skeleton pipeline skripti i zajednicki Spark session builder
3. Bronze implementacija i metadata
4. Silver transformacije i partition write
5. Gold agregacije
6. Notebook vizualizacije
7. CI workflow
8. README finalizacija
