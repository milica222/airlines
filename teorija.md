*Apache Spark* je sistem za distribuiranu obradu podataka. Umesto da jedan računar obradi sve podatke, Spark koristi klaster, odnosno grupu računara koji rade zajedno.

                DRIVER
                   |
            Cluster Manager
             /     |      \
            /      |       \
      Worker 1  Worker 2  Worker 3
          |        |         |
      Executor  Executor  Executor
       tasks     tasks      tasks

*Driver* je glavni proces Spark aplikacije. On izvršava tvoj glavni program, prati šta želiš da uradiš i organizuje posao. Spark aplikacija zatim preko *Cluster Manager-a* dobija resurse na računarima u klasteru. Na *worker* računarima pokreću se *Executors*, a executori zapravo izvršavaju taskove i mogu da čuvaju podatke u memoriji.

Spark prvo analizira šta želiš da uradiš. Ne kreće odmah da izvršava svaku liniju, već formira plan izvršavanja. Kada naiđe na operaciju koja zahteva rezultat, pokreće obradu. To se naziva *lazy evaluation*.

*RDD = Resilient Distributed Dataset.*
Resilient   → može da se oporavi ako neki računar otkaže
Distributed → podaci su raspoređeni na više računara
Dataset     → kolekcija podataka

RDD je, uprošćeno, velika kolekcija podataka podeljena na više delova koji mogu paralelno da se obrađuju. Spark dokumentacija ga definiše kao kolekciju elemenata podeljenu između čvorova klastera, tako da se nad njima mogu paralelno izvršavati operacije.
RDD je immutable - Kada napraviš RDD, ne menjaš postojeći RDD. NPR Ako imaš: rdd2 = rdd.map(lambda x: x * 2), to nije promenjen rdd  vec dobijaš novi. To Spark-u mnogo olakšava distribuiranu obradu i oporavak od grešaka.

Operacije nad RDD-om se uglavnom dele na dve grupe - Transformations i Actions.
Transformations prave novi RDD: map, filter, flatMap, distinct, reduceByKey
Actions zahtevaju konkretan rezultat: count, collect, first, reduce, save

Lineage — veoma bitna osobina RDD-a - Spark pamti kako je RDD nastao. Ako se izgubi Partition 3 od RDD3, Spark ne mora obavezno da čuva rezervnu kopiju svakog međurezultata. Može da pogleda lineage i ponovo izračuna izgubljenu particiju. Zato je RDD resilient.
RDD1
 ↓ filter
RDD2
 ↓ map
RDD3
 ↓ reduceByKey
RDD4

Cache / persist - Ako isti RDD koristiš više puta, možeš da kažeš rdd.cache(). Spark tada pokušava da ga zadrži u memoriji, umesto da ga svaki put ponovo računa. Upravo je mogućnost efikasnog ponovnog korišćenja podataka jedna od važnih karakteristika Spark-a.
RDD
 ↓
operacija A

RDD
 ↓
operacija B

RDD
 ↓
operacija C

MapReduce

MapReduce je model distribuirane obrade podataka.  Najlakše se razume preko brojanja reči. Map uzima podatke i pravi parove. Shuffle + Sort - Sistem grupiše iste ključeve, pa se prebace preko mreže sa jednog računara na drugi  (shuffle). Reducer sabira i dobijamo konacan rezultat. Hadoop MapReduce automatski deli ulaz na delove, pokreće map taskove paralelno, sortira njihove rezultate i prosleđuje ih reduce taskovima. Takođe prati taskove i može ponovo da pokrene one koji nisu uspeli.  



Klaster i podela jobova  

Klaster je jednostavno grupa računara koji rade kao jedna celina.  U Spark-u je veoma važno razlikovati:  Application -> Job -> Stage -> Task  

1 JOB
   ↓
Stage 1
 ├ Task 1
 ├ Task 2
 ├ Task 3
 └ ...

Stage 2
 ├ Task 1
 ├ Task 2
 └ ...

Zašto Spark deli Job na Stage-ove? Ovo je vezano za veoma važnu razliku između: narrow dependency i wide dependency.