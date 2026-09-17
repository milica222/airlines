# About: Big Data osnove i kako se uklapaju u Swiss Parking projekat

Ovaj dokument je teorijsko-prakticni vodic za predmet "obrada velike kolicine podataka", sa fokusom na:
1. sta je Spark
2. sta je Parquet
3. Spark arhitektura
4. RDD detalji
5. MapReduce paradigma
6. klasterizacija i podela poslova (job decomposition)
7. task scheduling
8. Hadoop arhitektura
9. kako se sve to direktno povezuje sa ovim projektom

---

## 1) Zasto Big Data pipeline uopste postoji

Kod malih dataset-a mozes sve da uradis u jednoj skripti i jednom DataFrame-u u memoriji. Kod velikih dataset-a to puca zbog:
1. ogranicene RAM memorije na jednom racunaru
2. predugog vremena obrade na jednom CPU-u
3. potrebe za ponovljivom i pouzdanom obradom
4. potrebe za odvojenim slojevima: sirovo, ocisceno, analiticko

Zato uvodimo:
1. distribuiranu obradu (Spark)
2. kolonarni format za analitiku (Parquet)
3. data lake slojeve (Bronze/Silver/Gold)
4. orkestraciju i validaciju pipeline-a

---

## 2) Sta je Apache Spark

Apache Spark je distribuirani engine za obradu podataka, dizajniran da radi:
1. in-memory kada je moguce
2. paralelno preko vise executora i CPU jezgara
3. na klasteru (vise masina ili vise kontejnera)

Spark API slojevi:
1. RDD API (nizak nivo, funkcionalni stil)
2. DataFrame API (struktuirani podaci, SQL optimizacija)
3. Spark SQL (deklarativni SQL nad DataFrame-ovima)
4. Structured Streaming (stream obrada)
5. MLlib / GraphX (ML i grafovi)

U ovom projektu koristimo DataFrame + Spark SQL nivo, jer je najprikladniji za ETL i agregacije.

---

## 3) Spark arhitektura (cluster view)

Klasicna Spark arhitektura ima sledece komponente:
1. Driver
2. Cluster Manager
3. Executors
4. Tasks

### 3.1 Driver

Driver je "mozak" aplikacije:
1. pokrece SparkSession
2. pravi DAG (Directed Acyclic Graph) operacija
3. deli posao na stages i tasks
4. salje taskove executorima
5. skuplja rezultate i metadata informacije

U ovom projektu, svaka skripta iz src/ kada se pokrene (`download.py`, `bronze_to_silver.py`, `silver_to_gold.py`, `validate_outputs.py`) ima svoj driver proces.

### 3.2 Cluster Manager

Cluster Manager rasporedjuje resurse:
1. Spark Standalone
2. YARN
3. Kubernetes

U ovom projektu koristimo Spark Standalone model kroz Docker Compose:
1. `spark-master` servis
2. `spark-worker` servis

### 3.3 Executors

Executor je proces koji izvrsava taskove i cuva podatke u memoriji/diska cache-u.

### 3.4 Tasks

Task je najmanja jedinica rada i obicno obradjuje jednu particiju podataka.

---

## 4) RDD detaljnije

RDD (Resilient Distributed Dataset) je osnovna Spark apstrakcija.

Ključne osobine RDD-a:
1. immutable (ne menja se, svaka transformacija vraca novi RDD)
2. distribuiran po particijama
3. resilient (moze da se rekonstruiše preko lineage grafa)
4. lazy evaluation (transformacije se ne izvrsavaju dok ne dodje akcija)

### 4.1 Transformacije i akcije

Transformacije (lazy):
1. `map`
2. `filter`
3. `flatMap`
4. `reduceByKey`

Akcije (trigger):
1. `count`
2. `collect`
3. `saveAsTextFile`
4. `take`

DataFrame API interno i dalje koristi koncept particija, DAG-a i taskova koji poticu iz RDD modela. Drugim recima, iako u kodu ne pises direktno RDD, Spark engine radi po istim osnovnim principima.

### 4.2 Lineage i fault tolerance

Spark cuva lineage (kako je dataset nastao). Ako executor izgubi particiju, Spark moze da ponovo izracuna samo taj deo, umesto ceo posao.

Ovo je vazno za velike obrade, jer smanjuje potrebu za skupim full restart-om posla.

---

## 5) MapReduce paradigma i odnos sa Spark-om

MapReduce je klasicni model iz Hadoop ekosistema:
1. Map faza transformise ulaz u key-value parove
2. Shuffle/Sort grupise parove po kljucu
3. Reduce faza agregira vrednosti po kljucu

Spark nije isto sto i Hadoop MapReduce, ali je konceptualno kompatibilan:
1. `groupBy` + `agg` u Spark-u podrazumeva shuffle
2. operacije po kljucu su "map/reduce-like"

Primer iz projekta:
1. `groupBy("canton").agg(sum(...))` u Gold sloju je prakticno reduce po kljucu `canton`
2. pre toga transformacije i normalizacije u Silver sloju su map-like koraci

---

## 6) Klasterizacija i podela jobova

Kada Spark dobije kod, proces ide ovako:
1. logicke operacije postaju DAG
2. DAG se deli na stages
3. svaki stage se deli na tasks po particijama
4. tasks se rasporedjuju na dostupne executore

### 6.1 Sta je stage granica

Stage se obicno prekida na shuffle granici.

Bez shuffle (narrow transformations):
1. `select`
2. `withColumn`
3. `filter`

Sa shuffle (wide transformations):
1. `groupBy`
2. `join`
3. `distinct`

U projektu:
1. Silver faza ima vise narrow transformacija (izvlačenje kolona, filter koordinata)
2. Gold faza ima wide transformacije (groupBy agregacije), pa tu Spark pravi izrazenije stage granice

### 6.2 Particije

Particionisanje je kljuc paralelizma. Vise particija obicno znaci bolja raspodela rada, ali previse particija moze da doda overhead.

U projektu je `spark.sql.shuffle.partitions` eksplicitno podeseno kroz env varijablu i `spark_utils.py`.

---

## 7) Task scheduling u Spark-u

Spark scheduler radi u dva sloja:
1. DAGScheduler
2. TaskScheduler

### 7.1 DAGScheduler

DAGScheduler:
1. pravi stages iz DAG-a
2. odredjuje dependency veze
3. planira retry kod failure-a

### 7.2 TaskScheduler

TaskScheduler:
1. rasporedjuje taskove na executore
2. uzima u obzir lokalnost podataka gde je moguce
3. upravlja retry mehanizmom taskova

### 7.3 Zasto ovo tebi znaci

Prakticno, kada pokrenes pipeline, Spark sam radi scheduling. Tvoj posao je da:
1. drzis transformacije ciste i predvidive
2. ogranicis nepotrebne shuffles
3. kontrolises broj particija i memoriju executora

To vec radimo preko konfiguracije u `spark_utils.py` i kroz odvojen ETL dizajn.

---

## 8) Sta je Parquet i zasto je bitan

Parquet je kolonarni format skladistenja podataka.

Prednosti Parquet-a:
1. kolonarno citanje (citas samo potrebne kolone)
2. bolja kompresija
3. schema metadata
4. efikasniji za analiticke upite

U odnosu na JSON:
1. JSON je odlican kao sirovi ulaz (fleksibilan, ali sporiji za analitiku)
2. Parquet je odlican za ciscen i analiticki sloj

Zato pipeline radi:
1. Bronze: JSON
2. Silver/Gold: Parquet

---

## 9) Hadoop arhitektura (osnove)

Hadoop ekosistem istorijski obuhvata:
1. HDFS (storage)
2. YARN (resource management)
3. MapReduce (processing)

### 9.1 HDFS

Distribuirani fajl sistem:
1. NameNode cuva metadata
2. DataNode cuvaju blokove podataka
3. podaci su replicirani radi otpornosti

### 9.2 YARN

ResourceManager + NodeManager model za raspodelu CPU/RAM resursa aplikacijama.

### 9.3 MapReduce

Batch processing model (map -> shuffle -> reduce), pouzdan ali sporiji od modernijeg in-memory pristupa Spark-a.

### 9.4 Gde je Spark u ovoj prici

Spark moze da radi:
1. iznad YARN-a
2. iznad Kubernetes-a
3. u Standalone modu

U ovom projektu je Standalone u Docker-u, ali konceptualno isti ETL moze da se prebaci na YARN/K8s u vecim sistemima.

---

## 10) Kako se teorija uklapa u tvoj projekat

Ovde je direktno mapiranje teorije na implementaciju:

1. Data lake slojevi
1. Bronze = sirovi JSON
2. Silver = ciscenje + standardizacija + quality
3. Gold = agregati za analizu

2. Spark arhitektura
1. Driver se pokrece kroz svaku Python ETL skriptu
2. Master/Worker su u `docker-compose.yml`
3. Executors izvrsavaju taskove i obrade particije

3. RDD/MapReduce koncepti
1. Silver transformacije su map-like
2. Gold agregacije su reduce-like sa shuffle korakom

4. Scheduling i job decomposition
1. Spark automatski deli DataFrame plan u stages/tasks
2. shuffle operacije (`groupBy`) uvode stage granice

5. Format podataka
1. JSON ulaz zbog fleksibilnosti
2. Parquet izlaz zbog analiticke efikasnosti

6. Kvalitet i pouzdanost
1. Silver quality report meri drop/null metrike
2. `validate_outputs.py` proverava da su Silver/Gold izlazi validni

---

## 11) End-to-end tok obrade u ovom projektu

Korak 1. Ingest (Bronze)
1. `src/download.py` ucitava ili skida ulazni JSON
2. cuva raw snapshot/latest
3. cuva metadata fajlove

Korak 2. Transform (Silver)
1. `src/bronze_to_silver.py` flattenuje GeoJSON
2. deduplikuje po `parking_id`
3. filtrira koordinate van granica CH
4. standardizuje parking tip
5. racuna kapacitete i wheelchair dostupnost
6. mapira `canton`
7. pise partitioned parquet + quality report

Korak 3. Aggregate (Gold)
1. `src/silver_to_gold.py` racuna trazene agregate
2. pise 4 Gold dataset-a

Korak 4. Validate
1. `src/validate_outputs.py` proverava postojanje i ne-praznost izlaza

Korak 5. Orchestrate
1. `src/pipeline.py` pokrece sve korake redom i loguje trajanje

---

## 12) Generalni princip obrade velikih podataka

Bez obzira na alat, standardni pattern je skoro uvek isti:
1. ingest sirovih podataka
2. data quality i schema stabilizacija
3. semanticka standardizacija
4. particionisano cuvanje u analitickom formatu
5. agregacije po poslovnim pitanjima
6. validacija izlaza
7. vizualizacija i/ili serving sloj
8. automatizacija i reproducibilnost

Tvoj projekat prati upravo taj industrijski pattern i zato je dobar primer za predmet.

---

## 13) Brza terminologija za usmeni/ispit

1. Driver: kontrolni proces Spark aplikacije.
2. Executor: proces koji izvrsava taskove.
3. Task: najmanja jedinica rada po particiji.
4. Stage: skup taskova bez shuffle granice.
5. Shuffle: redistribucija podataka po kljucu izmedju executora.
6. RDD: osnovna distribuisana immutable kolekcija.
7. DataFrame: tabelarni API iznad Spark engine-a.
8. Parquet: kolonarni format za efikasnu analitiku.
9. HDFS: distribuirani storage iz Hadoop-a.
10. YARN: resource manager u Hadoop ekosistemu.

---

## 14) Zakljucak

Ovaj projekat nije samo tehnicki ETL zadatak, vec mini model realnog Big Data sistema:
1. ima slojevitu arhitekturu
2. koristi distribuirani engine
3. koristi analiticki format
4. ima quality i acceptance kontrole
5. ima automatizaciju kroz CI i Docker reproducibilnost

To je tacno ono sto se trazi na predmetu obrade velike kolicine podataka: razumevanje i implementacija celog procesa, od sirovog ulaza do analitickog izlaza.
