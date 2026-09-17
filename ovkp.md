## Introduction

Uvod u Big Data sisteme: Arhitektura, Izazovi i Modeli (ETH Zurich Vodič)

1. Revolucija Podataka i Informaciono Društvo

U savremenom informacionom društvu, ključni izazov više nije samo prikupljanje podataka, već njihova transformacija u konkretnu vrednost. Ovaj proces zahteva duboko razumevanje paradigmi koje omogućavaju orkestraciju tehnologija u kompleksnim ekosistemima.

Put od sirovog podatka do vrednosti:

* Podaci \rightarrow Informacije \rightarrow Znanje \rightarrow Vrednost

Četvrta paradigma (data-driven science): Big Data revolucija označava prelazak na nauku zasnovanu na podacima. U ovoj paradigmi, naučna otkrića, novi proizvodi i poslovni modeli ne nastaju isključivo iz teorijskih pretpostavki, već direktnom analizom masivnih, heterogenih setova podataka koji dolaze velikom brzinom i u različitim oblicima.

2. Izazovi Skaliranja: Zettabyte Razmera

Količina digitalnih informacija danas dostiže Zettabyte razmeru (broj sa 21 nulom) na godišnjem nivou. Naša sposobnost da generišemo podatke raste eksponencijalno brže od procesorske moći tradicionalnih sistema, što zahteva promenu pristupa samoj strukturi podataka.

Kao što profesor Ghislain Fourny ističe u kurikulumu: "No data is harmed during this course, however, please be psychologically prepared that our data may not always be in third normal form."

Zašto podaci danas često napuštaju "Treću normalnu formu" (3NF):

* Heterogenost: Podaci pristižu iz hiljada neusklađenih izvora i nemaju jedinstvenu šemu.
* Brzina (Velocity): Rigidna normalizacija i provera integriteta usporavaju upis kod ekstremno brzih tokova.
* Performanse distribucije: U distribuiranim sistemima, denormalizacija se koristi namerno kako bi se izbegli skupi "Join" procesi preko mreže.
* Messy data: Realnost Big Data sveta su polustrukturirani podaci koji se ne uklapaju u stroge relacione okvire.

3. Evolucija Sistema: Od Monolita do Distribuiranih Klastera

Moderni Big Data stack nastao je "razbijanjem" monolitnog RDBMS modela iz 1970-ih, koji je bio optimizovan za jednu mašinu, i njegovom ponovnom izgradnjom na klasterima.

Metode skaliranja:

* Scale up (Vertikalno): Dodavanje resursa (RAM, CPU) na jednu mašinu. Ograničeno fizičkim limitima i ekstremno skupo.
* Scale out (Horizontalno): Povezivanje velikog broja standardnih mašina (commodity hardware) u klaster. Ovo je osnova moderne skalabilnosti jer omogućava linearni rast kapaciteta uz značajne uštede.

Parametar	Relacione baze (RDBMS)	Distribuirani sistemi (Big Data)
Skalabilnost	Single machine (Scale up)	Cluster (Scale out)
Održavanje	Standardno / Centralizovano	Visoka kompleksnost i troškovi
Cena	Visoka (specijalizovan hardver)	Niža po jedinici (commodity hardware)

4. Arhitektonska Hijerarhija: Fizičko vs. Logičko Skladištenje

ETH klasifikacija insistira na jasnom razgraničenju između toga kako se podaci čuvaju (bitovi na disku) i kako su logički organizovani za korisnika.

Fizičko skladištenje

Slojevi zaduženi za distribuciju bajtova preko čvorova u klasteru.

* HDFS: Distribuirani fajl sistem za čuvanje masivnih fajlova (npr. CSV, Parquet).
* Object Storage (S3): Skladištenje podataka kao objekata sa metapodacima, idealno za cloud okruženja.
* Key-value stores: Sistemi optimizovani za ultra-brzi pristup podacima putem jedinstvenog ključa.

Logičko skladištenje

Slojevi koji definišu strukturu podataka radi lakšeg upita i analize.

* Document stores: Skladištenje polustrukturiranih stabala (npr. MongoDB).
* Column stores: Optimizovani za analitičke upite nad specifičnim setovima kolona (npr. HBase).
* Graph databases: Fokus na kompleksnim odnosima i vezama među entitetima (npr. Neo4j).
* Data warehouses (npr. ROLAP): Sistemi za višedimenzionalnu analizu koji predstavljaju implementaciju modela Kocke (Cubes).

5. Pregled Modela Podataka (Shapes and Models)

U Big Data svetu, oblik podataka diktira izbor tehnologije. Kurikulum identifikuje četiri osnovna oblika:

1. Tabele (Tables): Dvodimenzionalna struktura redova i kolona. Tehnologija: Relacioni model / SQL.
2. Stabla (Trees): Hijerarhijski podaci, idealni za denormalizaciju. Tehnologija: JSON, XML.
3. Grafovi (Graphs): Entiteti (čvorovi) i njihove međusobne veze (ivice). Tehnologija: Neo4j, Cypher.
4. Kocke (Cubes): Višedimenzionalni podaci optimizovani za agregacije. Tehnologija: OLAP, MDX.

6. Paradigma Wide Column Stores i HBase

HBase je dizajniran da pruži performanse u realnom vremenu nad masivnim tabelama, radeći direktno iznad HDFS-a na klasterima standardnog hardvera. Njegov dizajn prati ključnu BigTable paradigmu: "Store together what is accessed together" (Skladišti zajedno ono čemu se zajedno pristupa).

Poređenje performansi na osnovu arhitektonskih karakteristika:

Parametar	Wide Column Stores	Object Stores	RDBMS	HDFS	Key-value
High Throughput	+	+	-	+	-
Low Latency	+	-	+	-	+
Updates	+	-	+	-	+
Larger values	+	+	+	+	-
Larger collections	+	+	-	+	+
Random Access	+	-	+	-	+
Range Access	+	-	+	+	-

Legenda: (+) Visoke performanse/Podržano; (-) Niske performanse/Nije podržano

7. Programski Jezici i Paradigme Upita

Prelazak na Big Data donosi promenu sa funkcionalnog na deklarativni pristup programiranju.

* Funkcionalno (How): Korisnik mora da definiše tačan redosled koraka za obradu (često se koristi u MapReduce).
* Deklarativno (What): Korisnik definiše šta želi da dobije (npr. SQL, JSONiq), a sistem preuzima odgovornost za optimizaciju izvršavanja preko celog klastera. Ovo omogućava apstrakciju kompleksnosti distribuiranog okruženja.

Checklista za ispit (Ključne operacije):

* [ ] Selection: Filtriranje elemenata na osnovu uslova.
* [ ] Projection: Izolacija specifičnih atributa ili kolona.
* [ ] Joining: Kombinovanje podataka iz različitih izvora (naročito kompleksno u Big Data).
* [ ] Grouping: Agregacija podataka radi dobijanja uvida.
* [ ] Ordering & Windowing: Sortiranje i analitika nad vremenskim ili logičkim prozorima.

8. Zaključak: Od Inženjeringa do Poslovne Vrednosti

Suština Big Data inženjeringa nije u poznavanju svakog alata pojedinačno, već u sposobnosti njihove orkestracije. Inženjer mora razumeti sisteme "u malom" (detalji implementacije HBase-a ili Spark-a) i "u velikom" (kako se podaci kreću kroz data centar).

1. Paradigme ispred tehnologija: Alati poput MongoDB-a ili HBase-a mogu zastareti, ali principi distribuiranog skladištenja i modelovanja (Trees, Graphs) su trajni.
2. Orkestracija je ključ: Nijedan sistem ne rešava sve probleme. Uspeh je u kombinovanju (npr. korišćenje HBase-a za brze upite preko HDFS-a za masovno skladištenje).
3. Arhitektura paralelizma: Razumevanje razlike između dvostepenog (MapReduce) i DAG-zasnovanog (Spark) paralelizma je ključno za efikasnu obradu podataka na nivou klastera.

## Cloud Storage

Ovaj izveštaj predstavlja detaljan pregled koncepta skladištenja u oblaku (Cloud Storage), sa posebnim fokusom na objektno skladištenje (Object Storage), zasnovan na materijalima sa predavanja o Big Data na ETH Zurich.

1. Konceptualni okvir skladištenja u Big Data ekosistemu

U okviru Big Data arhitekture, skladištenje je podeljeno na fizičke i logičke slojeve. Cloud Storage, konkretno Object Storage (čiji je primarni primer Amazon S3), predstavlja temeljnu komponentu fizičkog sloja skladištenja, pored distribuiranih sistema datoteka (HDFS) i key-value skladišta.

Glavni izazov savremenog informacionog društva je obrada podataka koji dolaze u ogromnim količinama (Zettabyte rang), različitih oblika i sa niskim stepenom strukture. Tradicionalni sistemi nisu u stanju da efikasno odgovore na ove zahteve, što je dovelo do razvoja novih arhitektura za skladištenje.

Problemi sa relacionim bazama podataka (RDBMS)

Tradicionalni RDBMS sistemi se suočavaju sa ozbiljnim ograničenjima u Big Data okruženju:

* Mali obim (Small scale): Dizajnirani su za ograničene količine podataka.
* Jedna mašina: Primarno su optimizovani za rad na jednom serveru.
* Poteškoće sa skaliranjem: Iako je moguće "vertikalno skaliranje" (Scale up), ono ima svoje fizičke i ekonomske granice. "Horizontalno skaliranje" (Scale out) kod RDBMS-a je izuzetno teško za implementaciju i nosi veoma visoke troškove održavanja.

2. Karakteristike Object Storage sistema

Object Storage je dizajniran da prevaziđe ograničenja tradicionalnih sistema pružajući visok stepen skalabilnosti i propusne moći.

Tehnički parametri i performanse

Na osnovu uporedne analize sistema skladištenja, Object Storage se odlikuje specifičnim performansama u odnosu na druge popularne sisteme (RDBMS, HDFS, Key-value skladišta):

Karakteristika	Object Storage (npr. S3)	RDBMS	HDFS	Key-value stores
Visoka propusna moć (Throughput)	+	-	+	-
Nisko kašnjenje (Latency)	-	+	-	+
Ažuriranje podataka (Updates)	-	+	-	+
Velike vrednosti (Larger values)	+	+	+	-
Velike kolekcije (Larger collections)	+	-	+	+
Nasumičan pristup (Random access)	-	+	-	+
Pristup opsegu (Range access)	-	+	+	-

Analiza prednosti:

1. Visoka propusna moć (High Throughput): Object Storage je izuzetno efikasan u prenosu velikih količina podataka, što ga čini idealnim za Big Data analitiku.
2. Upravljanje velikim objektima i kolekcijama: Za razliku od key-value skladišta koja preferiraju manje vrednosti, objektni sistemi su optimizovani za velike binarne objekte i masivne kolekcije podataka koje prevazilaze kapacitete jedne mašine.

Analiza ograničenja:

1. Visoko kašnjenje (Latency): Zbog mrežne infrastrukture i same arhitekture, vreme odziva za pojedinačne operacije je veće u poređenju sa lokalnim bazama podataka ili key-value skladištima.
2. Ograničena manipulacija podacima: Sistemi poput S3 nisu namenjeni čestim ažuriranjima (in-place updates) niti nasumičnom pristupu delovima objekta.
3. Nedostatak efikasnog pristupa opsegu: Za razliku od HDFS-a ili Wide Column skladišta (HBase), Object Storage nema ugrađenu optimizaciju za sekvencijalni pristup određenim opsezima podataka unutar objekata na isti način na koji to rade strukturirani sistemi.

3. Komparacija sa drugim sistemima

Object Storage vs. HDFS

Oba sistema nude visoku propusnu moć i podršku za velike kolekcije podataka. Međutim, glavna razlika je u arhitekturi i okruženju. HDFS je obično dizajniran da radi na "commodity" hardveru unutar klastera (često služeći kao podloga za HBase), dok je Object Storage servis u oblaku koji apstrahuje upravljanje hardverom i nudi elastičnije skaliranje.

Object Storage vs. Wide Column Stores (HBase)

Wide Column skladišta poput HBase-a, koja koriste HDFS kao fizički sloj, pokušavaju da kombinuju prednosti više sistema. Dok Object Storage gubi na performansama kod nasumičnog pristupa i ažuriranja, Wide Column sistemi su dizajnirani da omoguće:

* Visoku propusnu moć i nisko kašnjenje istovremeno.
* Efikasna ažuriranja.
* Nasumičan i opsežni pristup podacima.

Glavna paradigma dizajna kod naprednijih sistema (poput BigTable-a) koja nedostaje čistom objektnom skladištenju je: "Skladišti zajedno ono čemu se pristupa zajedno" (Store together what is accessed together).

4. Zaključak za pripremu ispita

Prilikom analize Cloud Storage rešenja, ključno je razumeti da ne postoji univerzalan sistem. Object Storage (S3) je primarno rešenje kada je potrebna:

1. Ekstremna skalabilnost za masovne količine podataka.
2. Visoka propusna moć za potrebe masovne paralelne obrade (poput MapReduce ili Spark procesa).
3. Skladištenje nepromenljivih (immutable) podataka ili velikih fajlova koji se retko menjaju.

S druge strane, za aplikacije koje zahtevaju nisko kašnjenje, često ažuriranje ili kompleksne upite nad malim delovima podataka, Object Storage mora biti dopunjen sistemima poput RDBMS-a, Document Store-a (MongoDB) ili Wide Column Store-a (HBase).

## Distributed File Systems

1. Uvod u Distributed File Systems (DFS) u Big Data steku

U okviru modernog tehnološkog steka za obradu velikih podataka, Distributed File Systems (DFS) predstavljaju temeljni sloj fizičkog skladištenja (Physical Storage), prema zvaničnoj ETH Zurich klasifikaciji. Ovaj sloj je konceptualno odvojen od sloja "logičkog skladištenja" (Logical Storage), gde spadaju Document ili Wide Column store sistemi.

HDFS (Hadoop Distributed File System) je nastao kao open-source implementacija principa prvi put dokumentovanih u Google-ovom naučnom radu o GFS-u (Google File System). Tradicionalni sistemi za upravljanje relacionim bazama podataka (RDBMS) projektovani su za "Single Machine" paradigmu, što ih čini neadekvatnim za gigantske količine neuređenih podataka. Primena RDBMS-a u klasterima je izuzetno teška za postavljanje (Hard to set up) i prati je veoma visoki trošak održavanja (Very high maintenance costs), zbog čega se industrija okrenula DFS rešenjima poput HDFS-a i Cloud rešenjima kao što je Amazon S3 (Object Storage).

2. Master-Slave Arhitektura: HDFS kao distribuirani sistem

Arhitektura HDFS-a je predikata na pretpostavci da je kvar hardvera uobičajena pojava, a ne izuzetak — tzv. "Failure as a first-class citizen" pristup. Sistem koristi Master-Slave model optimizovan za rad na standardnom hardveru (Commodity Hardware).

Namenode (Master)

Namenode je centralni autoritet i potencijalno usko grlo sistema. Njegove ključne karakteristike su:

* RAM-centric metapodaci: Namenode čuva celokupno stablo fajl sistema i mapiranje blokova isključivo u radnoj memoriji (RAM) radi brzine. Ispitna napomena: Ovo direktno limitira ukupan broj fajlova koje HDFS može podržati (tzv. "Small file problem").
* Kontrola pristupa i metapodaci: Upravlja metapodacima (Metadata) i usmerava klijente ka odgovarajućim Datanode-ovima.
* Komunikaciono opterećenje: Namenode može postati usko grlo kod operacija koje zahtevaju veliki broj malih zahteva zbog stalnih lookup-ova u metapodacima.

Datanodes (Slaves)

Datanodes su čvorovi zaduženi za fizičko skladištenje i izvršavanje I/O operacija.

* Skladištenje blokova: Čuvaju stvarne podatke na lokalnim diskovima.
* Heartbeat mehanizam (Signal o radu): Redovno šalju signale Namenode-u potvrđujući da su operativni. Ako signal izostane, Namenode pokreće proceduru oporavka podataka.

3. Particionisanje fajlova i Mehanizmi Otpornosti na Greške

HDFS koristi koncept deljenja fajlova na blokove fiksne veličine.

Logika veličine bloka (Block Size)

Standardne veličine bloka su 64MB ili 128MB. Zašto su blokovi u HDFS-u toliko veći od OS blokova (4KB)? Razlog je minimizacija vremena pozicioniranja glave diska (Seek time) u odnosu na vreme transfera podataka (Transfer time). Kod velikih blokova, vreme potrebno za prenos gigabajta podataka u potpunosti amortizuje inicijalno kašnjenje pri pronalaženju početka bloka.

Svest o rekovima (Rack Awareness) i replikacija

Otpornost na greške (Fault Tolerance) postiže se strategijom replikacije (standardno 3 kopije):

1. Prva replika: Na lokalnom čvoru.
2. Druga replika: Na drugom, udaljenom reku (Rack).
3. Treća replika: Na istom tom udaljenom reku, ali na različitom čvoru.

Ova polisa, poznata kao Svest o rekovima (Rack Awareness), ključna je za preživljavanje kvara na nivou celog reka (npr. otkaz "top-of-rack" mrežnog prekidača).

4. Analiza Performansi i Komparativna Metrika

HDFS je optimizovan za visoki protok (High Throughput) kroz serijsko čitanje, ali po cenu visoke latencije zbog overhead-a u komunikaciji sa Namenode-om.

Poređenje HDFS-a sa drugim sistemima skladištenja

Metrika	Object Storage	RDBMS	HDFS	Key-value stores	Wide column stores*
Throughput (Protok)	+	-	+	-	+
Latency (Latencija)	-	+	-	+	+
Updates (Ažuriranje)	-	+	-	+	+
Larger values (Velike vrednosti)	+	+	+	-	+
Larger collections (Velike kolekcije)	+	-	+	+	+
Random Access (Nasumični pristup)	-	+	-	+	+
Range Access (Pristup opsegu)	-	+	+	-	+

*Napomena: Wide Column sistemi (poput HBase-a) su projektovani da premoste jaz između HDFS-a i RDBMS-a, nudeći prednosti oba sveta kroz korišćenje HDFS-a kao podloge.

5. Princip Lokalnosti Podataka (Data Locality)

U tradicionalnim arhitekturama (Von Neumann), podaci se pomeraju ka procesoru. U Big Data svetu, zbog ogromnih volumena, ovo bi zagušilo mrežu. Lokalnost podataka (Data Locality) nalaže da se "kod pomera ka podacima".

Sistemi za masivnu paralelnu obradu (Massive Parallel Processing - MPP), kao što su MapReduce i Spark, šalju binarne izvršne fajlove (kod) direktno na Datanode koji čuva traženi blok.

Senior Assistant Pro-Tip: Ovo je osnovni razlog zašto u Big Data svetu ne koristimo mrežna skladišta poput NAS-a (Network Attached Storage). Kod NAS-a su procesiranje i skladištenje razdvojeni mrežom, što onemogućava lokalnost i stvara nepremostivo usko grlo pri analizi petabajta podataka.

6. Ključne definicije za ispit (Rezime)

* Veličina bloka (Block Size): Veliki fiksni segmenti (64MB+) optimizovani da minimizuju disk seek time u odnosu na transfer time.
* Faktor replikacije (Replication Factor): Broj redundatnih kopija podataka (obično 3) radi osiguranja otpornosti na greške.
* Metapodaci (Metadata): Podaci o strukturi fajlova koje Namenode drži u RAM-u, što predstavlja kritičnu tačku skalabilnosti.
* Protok (Throughput): Mera količine podataka obrađenih u jedinici vremena; primarna metrika za HDFS.
* Svest o rekovima (Rack Awareness): Strategija postavljanja replika blokova u različite fizičke ormare (rekove) radi zaštite od mrežnih kvarova.
* Signal o radu (Heartbeat): Periodična poruka koju Datanode šalje Namenode-u kao potvrdu dostupnosti.
* MPP (Massive Parallel Processing): Arhitektura koja omogućava simultano procesiranje podataka na stotinama čvorova, koristeći lokalnost podataka.
* Commodity Hardware: Pristupačni, komercijalni serveri na kojima se bazira ekonomičnost HDFS klastera.

## Wide Column Stores

1. Uvod u Wide Column Stores i HBase genezu

HBase je nastao kao distribuirana, skalabilna baza podataka otvorenog koda, direktno modelovana prema Google-ovom rešenju BigTable (2006), koje je definisalo temelje modernih Big Data sistema kroz svoj fundamentalni naučni rad ("Founding paper"). Projektovan je da prevaziđe ograničenja tradicionalnih RDBMS sistema, koji se suočavaju sa čvrstim limitima pri "Scale-up" pristupu (nadogradnja jedne mašine) i ekstremno visokim troškovima održavanja i kompleksnošću pri pokušajima "Scale-out" arhitekture (klasterizacija).

Osnovna paradigma dizajna HBase-a je "store together what is accessed together" (čuvaj zajedno ono čemu se zajedno pristupa). Sistem je po dizajnu predviđen za rad na velikim klasterima standardnog hardvera (commodity hardware), koristeći HDFS (Hadoop Distributed File System) kao podlogu za perzistentno skladištenje.

Sledeća tabela, bazirana na ETH Zurich analizi, poredi HBase sa alternativnim modelima skladištenja:

Kriterijum	RDBMS	HDFS	Key-value storovi	HBase (Wide Column)
Throughput (Propusnost)	Niska	Visoka	Niska	Visoka
Latency (Latencija)	Niska	Visoka	Niska	Niska
Updates (Ažuriranja)	Da	Ne	Da	Da
Random Access (Nasumičan pristup)	Da	Ne	Da	Da
Range Access (Pristup opsegu)	Da	Da	Ne	Da

2. Logički model podataka

HBase koristi tabelarni model koji je optimizovan za izbegavanje "expensive joins" (skupih operacija spajanja) karakterističnih za RDBMS. Umesto normalizacije, podaci se denormalizuju u široke redove, čime se spajanje podataka vrši u "write-time" (vreme upisa) kroz grupisanje, umesto u "query-time" (vreme upita).

Row ID i Column Families

Pristup podacima se vrši preko Row ID-a, koji služi kao primarni ključ za sortiranje i particionisanje. Logička struktura se dalje grana na:

* Column Families (Familije kolona): Predstavljaju osnovnu jedinicu izolacije i kompresije. Shema na nivou familija mora biti definisana unapred. One fizički grupišu podatke kako bi se omogućio efikasan pristup srodnim atributima.
* Column Qualifiers (Kvalifikatori kolona): Unutar svake familije, kolone se dodaju dinamički. Ovi kvalifikatori omogućavaju HBase-u da bude "schemaless" na nivou individualnih kolona, pružajući fleksibilnost u radu sa heterogenim podacima.

Verzionalnost i KeyValue struktura

Podaci nisu prosti parovi, već su organizovani kao višedimenzionalne mape. Svaka ćelija je zapravo niz verzija istog podatka identifikovanih preko vremenskog pečata (Timestamp). Na najnižem nivou, podatak je definisan kompleksnim KeyValue parom gde je ključ kompozit: Key = Row ID + Column Family + Column Qualifier + Timestamp

3. Hijerarhijska Arhitektura Sistema

Arhitektura HBase-a jasno razdvaja operacije upravljanja od operacija nad podacima, koristeći slojevitu strukturu iznad HDFS-a.

Control Plane vs. Data Plane

* HMaster (Control Plane): Odgovoran za administrativne i DDL operacije (kreiranje/brisanje tabela). Njegova ključna uloga je upravljanje meta-podacima i koordinacija regiona, odnosno dodeljivanje regiona odgovarajućim RegionServerima.
* RegionServer (Data Plane): Snaga sistema koja direktno opslužuje klijente. Svaki RegionServer je odgovoran za I/O operacije (čitanje/upis) nad podacima koji pripadaju regionima kojima on upravlja.

Hijerarhija skladištenja

Logička tabela se fizički distribuira kroz sledeću hijerarhiju:

* Table (Logički entitet)
  * Region (Horizontalna particija, opseg redova)
    * Store (Jedan po Column Family unutar regiona)
      * HFile (Finalni, sortirani format fajla na HDFS-u)

4. LSM-Tree Mehanizam i Životni ciklus upisa

HBase koristi Log-Structured Merge-tree (LSM) mehanizam kako bi rešio problem sporih nasumičnih upisa na disk. Glavna motivacija LSM-a je pretvaranje nasumičnih upisa u sekvencijalne upise, čime se drastično povećava propusnost.

Putanja upisa (Write Path)

1. Write-Ahead Log (WAL): Podatak se prvo upisuje u WAL na HDFS-u radi osiguranja trajnosti (durability) i oporavka u slučaju otkaza.
2. MemStore: Podatak se skladišti u in-memory bafer (MemStore), gde se automatski sortira.
3. Acknowledge: Klijent dobija potvrdu o uspešnom upisu odmah nakon što je podatak bezbedan u MemStore-u, bez čekanja na upis u HFile.

Flush proces (Pražnjenje memorije)

MemStore se periodično perzistira na disk u formi novih HFile-ova. Ovaj proces se pokreće pod tri specifična uslova:

* Dostizanje maksimalne veličine individualnog MemStore-a.
* Dostizanje ukupnog (overall) maksimalnog kapaciteta svih MemStore-ova na RegionServeru.
* Kada Write-Ahead Log postane pun (reaching full WAL).

5. Fizičko skladištenje: Od Regiona do HDFS-a

Fizička organizacija je ključ za horizontalno skaliranje sistema.

* Region: Definiše opseg redova (Row ID range) prema principu "Min-inclusive" (uključuje donju granicu) i "Max-exclusive" (isključuje gornju granicu). Kada region postane prevelik, on se automatski deli (split).
* Store: Fizička reprezentacija Column Family unutar regiona. Svaki Store sadrži jedan MemStore i nula ili više HFile-ova.
* HFile: Binarni format skladištenja na HDFS-u. Podaci su u HFile-u organizovani kao sortirani nizovi bajtova KeyValue zapisa, što omogućava da sistem bude ograničen brzinom sekvencijalnog prenosa (Transfer-time-bound), a ne brzinom pretraživanja diska.

6. Optimizacije i Analiza Performansi

Kompakcija (Compaction)

Budući da svaki Flush kreira novi HFile, broj fajlova na disku raste. Kompakcija je proces spajanja više HFile-ova u jedan veći, čime se smanjuje broj metapodataka i uklanjaju obrisani podaci ili stare verzije. HBase svesno prihvata kompleksnost kompakcije kako bi održao performanse sekvencijalnog I/O-a.

Bloom Filteri

Ovi probabilistički mehanizmi omogućavaju RegionServeru da preskoči čitanje HFile-ova za koje je siguran da ne sadrže traženi Row ID, drastično smanjujući broj nepotrebnih disk operacija.

Analiza uskih grla (Specialist View)

* Seek-time-bound: Tradicionalni RDBMS sistemi gde je performans ograničen brzinom kretanja glave diska (traženje podataka na različitim lokacijama).
* Transfer-time-bound: HBase (LSM sistemi) gde je, zahvaljujući sekvencijalnom rasporedu podataka, jedino ograničenje brzina kojom podaci mogu biti preneti sa diska u memoriju.

7. Rečnik ključnih pojmova (Glosar)

* WAL (Write-Ahead Log): Perzistentni dnevnik na HDFS-u koji beleži sve promene pre njihove obrade u memoriji.
* MemStore: Bafer u operativnoj memoriji gde se vrši sortiranje upisanih podataka pre prebacivanja na disk.
* HFile: Finalni, nepromenljivi (immutable) format fajla na HDFS-u koji sadrži sortirane KeyValue parove.
* Region: Horizontalna particija tabele, osnovna jedinica za distribuciju podataka na klasteru.
* Column Family: Logička grupacija kolona koja definiše fizički "Store" i parametre kompresije.
* HMaster: Centralni koordinator zadužen za DDL operacije i nadzor nad dodelom regiona.
* Column Qualifier: Dinamička kolona unutar familije, omogućava fleksibilno dodavanje atributa bez izmene sheme.

## Massive Parallel Processing (MPP) i MapReduce Arhitektura

1. Uvod u Massive Parallel Processing (MPP)

Tradicionalni sistemi za upravljanje relacionim bazama podataka (RDBMS) projektovani su za monolitni rad na jednoj mašini (single machine). U kontekstu sistema velikih podataka (Big Data), ovakva arhitektura predstavlja fundamentalno ograničenje usled nemogućnosti efikasnog skaliranja.

* Ekonomska neodrživost vertikalnog skaliranja (Scale-up): Povećanje performansi dodavanjem resursa na jednu mašinu prati eksponencijalni rast troškova za linearne dobitke u kapacitetu.
* Prednost horizontalnog skaliranja (Scale-out): Prelazak na MPP omogućava linearni rast troškova za linearne dobitke, koristeći klastere sačinjene od standardnog hardvera (commodity hardware).
* Arhitektonska uska grla: Tradicionalni sistemi pate od ograničene propusne moći diska i mrežne latencije kada se suoče sa petabajtima podataka.

Moderna distribuirana arhitektura, inspirisana HBase i BigTable filozofijom, nalaže promenu paradigme skladištenja:

"Store together what is accessed together" (Skladištite zajedno ono čemu se zajedno pristupa). Ovim se optimizuje lokalnost podataka i omogućava masovna paralelizacija na distribuiranim klasterima.

2. MapReduce Programski Model: Detaljna Anatomija

MapReduce je programski model duboko ukorenjen u principima funkcionalnog programiranja. Koristeći čiste funkcije bez sporednih efekata, sistem garantuje da se operacije mogu bezbedno izvršavati paralelno na hiljadama čvorova.

Map faza

U ovoj fazi, podaci se dele na particije (splits). Map funkcija transformiše ulazne sirove podatke u intermedijalne parove ključ-vrednost (key-value). Svaki podatak se obrađuje izolovano, što je ključ za masovnu paralelizaciju.

Shuffle & Sort faza (Mrežno usko grlo)

Ova faza je kritični "most" i predstavlja blocking phase – Reducer čvorovi ne mogu započeti rad dok se celokupan Shuffle proces ne završi.

* Particionisanje: Koristi se Hash funkcija nad ključem kako bi se odredilo na koji Worker čvor (Reducer) će određeni par biti poslat.
* Mrežni intenzitet: Podaci se grupišu po ključu i prenose kroz mrežu, što ovu fazu čini najskupljom operacijom u smislu mrežnog saobraćaja.

Reduce faza

Finalni korak gde se vrši agregacija. Funkcija prihvata listu vrednosti za svaki jedinstveni ključ i generiše konačni rezultat koji se upisuje nazad u distribuirani sistem datoteka (HDFS).

Tehnički pregled MapReduce toka podataka

Faza	Ulaz (Input)	Operacija	Izlaz (Output)
Map	Ulazni split (sirov)	Transformacija u K-V parove	Intermedijalni (Key, Value)
Shuffle & Sort	Intermedijalni parovi	Hash Partitioning i mrežni transfer	Grupisane liste po ključu
Reduce	Liste vrednosti po ključu	Agregacija i finalno procesiranje	Konačni rezultat (HDFS)

3. Arhitektura Izvršavanja: Master i Worker Čvorovi

Upravljanje resursima i koordinacija izvršavanja povereni su strogo definisanim ulogama:

Master čvor: Deluje kao centralni planer (scheduler). Odgovoran je za dodelu zadataka, praćenje progresa putem Heartbeats (statusnih signala koje šalju Workeri) i održavanje meta-podataka o poslu. Master rešava problem Stragglers-a (sporih radnih čvorova) putem Speculative Execution mehanizma – pokretanjem redundantne kopije sporog zadatka na drugom čvoru kako bi se preduhitrilo kašnjenje celog posla.

Worker čvorovi: Izvršne jedinice koje sprovode Map ili Reduce funkcije. Oni kontinuirano komuniciraju sa Masterom, signalizirajući svoju dostupnost i status zadataka. Ako Worker ne pošalje Heartbeat u definisanom roku, Master ga proglašava neispravnim i redistribuira njegove zadatke.

4. Integracija sa HDFS-om i Hijerarhija "Data Locality"

Sinergija između MapReduce modela i HDFS-a (Hadoop Distributed File System) rešava problem mrežnog zagušenja kroz paradigmu slanja koda ka podacima.

Koncept Data Locality (lokalnost podataka) podrazumeva da se Map zadaci dodeljuju onim čvorovima koji već poseduju potrebne blokove podataka na svojim lokalnim diskovima. Ova lokalnost je hijerarhijski organizovana kroz Rack Awareness (svest o topologiji mreže):

1. Isti čvor (Node-local): Kod se izvršava na istoj mašini gde su podaci (najveće performanse).
2. Isti rek (Rack-local): Ako je čvor zauzet, koristi se mašina u istom reku (minimalno mrežno kašnjenje).
3. Različit rek (Off-switch): Podaci se prenose između rekova (najskuplja opcija, izbegava se).

5. Kritička Analiza: Prednosti i Ograničenja

Prednosti

* Otpornost na greške (Fault tolerance): Zahvaljujući re-eksekuciji i mehanizmima poput Speculative Execution, sistem je imun na otkaze pojedinačnih čvorova.
* Ekonomična skalabilnost: Efikasan rad na hiljadama jeftinih mašina.

Ograničenja

* Pisanje na disk: Svaka faza MapReduce modela zahteva da se Intermediate Data (intermedijalni podaci) zapišu na lokalni disk Workera pre sledeće faze, što generiše ogroman I/O overhead.
* Visoka latencija: MapReduce nije pogodan za iterativne algoritme ili interaktivne upite zbog rigidnog dvostepenog modela, za razliku od Sparka koji koristi DAG (Directed Acyclic Graph) i procesiranje u memoriji.

6. Zaključak za pripremu ispita

Za uspešno polaganje ispita, student mora vladati sledećim konceptima:

1. Ekonomija skaliranja: Razlika između eksponencijalnih troškova vertikalnog i linearnih troškova horizontalnog skaliranja.
2. Shuffle Bottleneck: Razumevanje zašto je ovo blocking faza i uloga Hash Partitioning funkcije.
3. Speculative Execution: Kako Master rešava problem Stragglers-a pokretanjem redundantnih zadataka.
4. Hijerarhija lokalnosti: Prioritet izvršavanja (Node -> Rack -> Datacenter).
5. Intermediate Data: Shvatanje da je upis intermedijalnih podataka na disk glavni uzrok latencije u poređenju sa modernijim in-memory sistemima.
6. Funkcionalna paradigma: Zašto nedostatak side-effect-a omogućava determinističko ponovno izvršavanje u slučaju kvara.

##  Upravljanje resursima (Resource Management)

Ispitni izveštaj: Upravljanje resursima (Resource Management) u velikim klasterima

Ovaj izveštaj analizira ključne principe upravljanja resursima u modernim distribuisanim sistemima, sa posebnim osvrtom na YARN arhitekturu (Yet Another Resource Negotiator), oslanjajući se na materijale sa ETH Zurich (predavanja dr Ghislaina Fournyja).

1. Motivacija i potreba za upravljanjem resursima

U skladu sa akademskim okvirima katedre za Big Data, prelazak sa tradicionalnih sistema na moderne klastere nije samo tehnička promena, već paradigmatski skok. Kao što dr Fourny ističe, mi smo "razbili" monolitne relacione sisteme iz 1970-ih kako bismo ih ponovo izgradili na velikim klasterima mašina.

Multi-tenancy (višekorisnički rad) postaje imperativ u svetu gde se količina podataka meri u Zetabajtima (21 nula). U ovoj "četvrtoj paradigmi" (nauka zasnovana na podacima), statička particija resursa je neodrživa. Deljenje zajedničkog hardvera — CPU-a, memorije i diska — na hiljadama čvorova sastavljenih od standardnog, jeftinog hardvera (commodity hardware) zahteva dinamičko upravljanje kako bi se postigla maksimalna efikasnost.

Ključni razlozi za uvođenje Resource Management sloja:

* Efikasna iskorišćenost: Dinamička alokacija sprečava da resursi stoje besposleni, što je ključno jer podaci često nisu u "trećoj normalnoj formi" i zahtevaju kompleksnu, resursno intenzivnu obradu.
* Skalabilnost klastera: Omogućava horizontalno proširivanje (scale-out) dodavanjem novih čvorova (nodes) i rekova (racks) bez remećenja postojećih operacija.
* Heterogenost podataka: Podrška za rad sa različitim formatima (JSON, XML, CSV) i modelima koji koegzistiraju na istom fizičkom sloju.
* Izolacija i stabilnost: Sprečavanje situacija u kojima jedna aplikacija "guši" ostale, čime se osigurava stabilnost celog ekosistema.

2. YARN Arhitektura (Yet Another Resource Negotiator)

Prema materijalima sa ETH (Part 9), YARN predstavlja arhitektonski sloj koji razdvaja upravljanje resursima od same logike obrade podataka. On deluje kao operativni sistem klastera koji poznaje njegovu fizičku strukturu, uključujući svest o rasporedu po rekovima (rack-awareness).

ResourceManager (RM) i NodeManager (NM)

U ovoj hijerarhiji, ResourceManager deluje kao "globalni arbitar", dok NodeManager služi kao lokalni agent na svakom čvoru.

Karakteristika	ResourceManager (RM)	NodeManager (NM)
Opseg delovanja	Globalni (ceo klaster)	Lokalni (pojedinačni čvor)
Glavna uloga	Arbitraža i alokacija resursa	Nadzor čvora i upravljanje kontejnerima
Ključne komponente	Scheduler (Planer) i ApplicationsManager (ASM)	Monitoring resursa i izvršni agent
Funkcija	Odlučuje o prioritetima i dodeli	Prati potrošnju (CPU, RAM) i izveštava RM

3. Koncept kontejnera (Containers)

Kontejner je osnovna jedinica apstrakcije fizičkog hardvera. On omogućava izolaciju aplikativne logike od sirovog hardvera čvora.

"Kontejner predstavlja logičku inkapsulaciju resursa na čvoru, specifikovanu kroz udeo CPU jezgara i RAM memorije. NM nadgleda izvršavanje zadatka unutar kontejnera, osiguravajući da on ne prekorači dodeljene limite."

U sistemima kao što je HBase (Wide Column Store), kontejneri omogućavaju da Regionservers efikasno koriste HDFS sloj, upravljajući memorijskim strukturama (Memstore) unutar definisanih resursnih granica.

4. Proces izvršavanja aplikacije i uloga ApplicationMaster-a

Životni ciklus aplikacije u YARN okruženju prati strogo definisan protokol komunikacije:

1. Podnošenje (Submission): Klijent šalje zahtev ApplicationsManager-u unutar RM-a.
2. Inicijalizacija AM-a: RM pronalazi slobodan kontejner na klasteru i u njemu pokreće ApplicationMaster (AM).
3. Pregovaranje (Resource Request): AM, koji nosi specifičnu logiku framework-a (npr. Spark ili MapReduce), šalje detaljne zahteve RM-u za dodatnim kontejnerima.
4. Alokacija i pokretanje: RM dodeljuje resurse, a AM kontaktira relevantne NM-ove kako bi pokrenuo zadatke u dobijenim kontejnerima.
5. Monitoring i završetak: AM prati progres i status zadataka; po završetku posla, AM izveštava RM i oslobađa kontejnere nazad u zajednički bazen resursa.

5. Planiranje resursa (Scheduling Strategies)

Scheduler, kao komponenta RM-a, donosi odluke o raspodeli na osnovu sledećih strategija:

* FIFO (First In First Out):
  * Prednosti: Najjednostavnija implementacija.
  * Mane: Nepogodan za deljene klastere; jedan veliki posao može "zaključati" klaster.
* Capacity Scheduler:
  * Prednosti: Omogućava organizacijama da dele klaster kroz definisane redove (queues) sa garantovanim kapacitetom.
  * Mane: Potencijalno smanjena iskorišćenost ako određeni redovi nisu aktivni.
* Fair Scheduler:
  * Prednosti: Dinamički dodeljuje resurse tako da tokom vremena svi poslovi dobiju "fer" udeo (vremenski udeo).
  * Mane: Zahteva kompleksniju konfiguraciju prioriteta.

6. Multi-framework podrška i ekosistem

YARN-ova najveća snaga je u omogućavanju koegzistencije različitih paradigmi obrade na istoj infrastrukturi. Zahvaljujući razdvajanju resursa od logike, isti klaster mogu deliti:

* MapReduce: Tradicionalna dvostepena obrada podataka.
* Spark: Moderni sistem baziran na usmerenim acikličnim grafovima (DAG).
* HBase: Koji koristi resurse za upravljanje skladištenjem na vrhu HDFS-a.

Ova fleksibilnost opravdava titulu YARN-a kao "operativnog sistema za Big Data", jer on orkestrira tehnologije neophodne za pretvaranje sirovih podataka u vredno znanje.

7. Zaključne napomene za pripremu ispita

Kao rezime za ispit, zapamtite ove ključne tehničke parove:

* ResourceManager: ApplicationMaster (Globalno upravljanje vs. Logika specifične aplikacije).
* NodeManager: Container (Nadzor čvora vs. Izolovana jedinica resursa).
* Scale-out: Commodity Hardware (Proširivanje klastera korišćenjem standardnih mašina).
* Multi-tenancy: Resource Isolation (Višekorisnički rad kroz strogo razgraničenje resursa).
* Rack-awareness: Data Locality (Svest o fizičkom rasporedu čvorova radi optimizacije performansi).

## Generic Dataflow Management – SPARK 

Ispitni izveštaj: Arhitektura i mehanizmi Apache Spark sistema

Ovaj izveštaj analizira arhitekturu i operativne mehanizme Apache Spark sistema u okviru "Big Data for Engineers" nastavnog plana i programa ETH Zurich. Fokus je na razumevanju paradigmi koje su omogućile prelazak sa rigidnog MapReduce modela na fleksibilno, in-memory procesiranje, uz striktno poštovanje opsega kursa koji naglašava arhitekturalne principe nad specifičnim aplikacijama poput mašinskog učenja.

1. Evolucija obrade podataka: Od MapReduce-a ka Spark-u

Spark je nastao kao odgovor na fundamentalna ograničenja MapReduce modela, koji je dominirao ranom fazom Big Data ere. Ključni problem MapReduce-a bio je njegov rigidni, dvofazni pristup koji je primoravao sistem da upisuje međurezultate na HDFS (disk I/O) nakon svake faze, uz obaveznu replikaciju podataka radi tolerancije na greške, što je drastično povećavalo latenciju.

Aspekt	MapReduce	Apache Spark
Brzina	Usko grlo u disk I/O i mrežnom saobraćaju zbog replikacije međurezultata na HDFS.	In-memory procesiranje; podaci se zadržavaju u RAM-u, minimizujući I/O operacije.
Model programiranja	Strogo dvofazni (Map pa Reduce); zahteva kompleksno ulančavanje poslova.	Fleksibilni DAG (Directed Acyclic Graph) koji omogućava složene tokove podataka.
Latencija i iteracije	Visoka latencija; svaki korak zahteva čitanje/pisanje na disk, što je neefikasno za iterativne algoritme.	Niska latencija; optimizovano za ponovnu upotrebu istog skupa podataka bez napuštanja memorije.

2. RDD (Resilient Distributed Dataset): Srž Spark arhitekture

RDD predstavlja osnovnu apstrakciju podataka u Spark-u. Razumevanje ovog koncepta je ključno za razumevanje kako Spark balansira performanse i pouzdanost.

* Resilient (Otpornost): Za razliku od MapReduce-a koji otpornost postiže skupom replikacijom podataka na disk, RDD koristi lineage (poreklo). Sistem čuva logički graf transformacija, što omogućava rekonstrukciju izgubljenih particija bez potrebe za fizičkim kopijama.
* Distributed (Distribuiranost): Podaci su horizontalno particionisani preko klastera čvorova. Spark paralelizuje operacije nad ovim particijama, omogućavajući skalabilnost na hiljade čvorova.
* Dataset (Kolekcija podataka): RDD je imutabilna (nepromenljiva) kolekcija objekata. Ova nepromenljivost je fundamentalna za konzistentnost u distribuiranim sistemima, jer eliminiše probleme sinhronizacije stanja između čvorova.

3. Operativni model: Imutabilnost i Lazy Evaluation

Sparkov operativni model ne predstavlja samo skup funkcija, već strategiju optimizacije resursa klastera.

* Imutabilnost: Pošto su RDD-ovi nepromenljivi, Spark uvek može da se osloni na determinističko stanje podataka. Ovo je mehanizam koji omogućava lineage-based fault tolerance; ako jedan čvor otkaže, "recept" za kreiranje RDD-a je uvek isti.
* Lazy Evaluation (Lenja evaluacija): Spark ne izvršava transformacije odmah. Umesto toga, on gradi plan izvršavanja dok se ne pozove akcija. Ovo omogućava Query Optimizer-u da sagleda ceo lanac operacija i izvrši optimizacije poput Predicate Pushdown (filtriranje podataka što bliže izvoru) ili Column Pruning, čime se smanjuje količina podataka koja se učitava u memoriju.

4. Diferencijacija operacija: Transformacije i Akcije

Jasna distinkcija između transformacija i akcija je stub Spark-ovog DAG modela.

Tip operacije	Definicija	Primeri	Rezultat
Transformacije	Definišu novi RDD na bazi postojećeg; lenjo se evaluiraju.	map, filter, join, union, groupByKey	Novi RDD (Lineage se proširuje)
Akcije	Iniciraju stvarno izračunavanje i vraćaju rezultat.	collect, count, saveAsTextFile, reduce	Vrednost u Driver programu ili side-effect na disku

5. DAG (Directed Acyclic Graph) i optimizacija izvršavanja

Spark interpretira niz transformacija kao DAG, što mu daje značajnu prednost u odnosu na MapReduce.

* Pipelining i Stage-ovi: DAG omogućava Spark-u da grupiše transformacije. Operacije sa "uskim zavisnostima" (Narrow Dependencies), poput map i filter, mogu se izvršiti u jednom prolazu nad podacima unutar istog Stage-a. Ovo se naziva pipelining i eliminiše potrebu za upisom na disk između operacija.
* Smanjenje disk I/O: Dok MapReduce mora da završi celu Map fazu pre nego što počne Reduce, Spark-ov DAG dozvoljava podacima da teku kroz graf transformacija u memoriji dokle god ne dođe do tačke mešanja podataka (shuffle), čime se drastično smanjuje overhead.

6. In-Memory Processing i performanse u akademskom kontekstu

Visoke performanse Spark-a (do 100x brži od MapReduce-a) proističu iz efikasnog korišćenja RAM-a za iterativne procese. Prema ETH Zurich materijalima, iako su Large scale analytics i Machine Learning izvan opsega ovog kursa, arhitekturalna prednost Spark-a je najbolje vidljiva upravo u iterativnim algoritmima gde se nad istim podacima vrši više krugova procesiranja.

Spark omogućava da se podaci eksplicitno keširaju u memoriji, izbegavajući ponovno čitanje sa HDFS-a u svakoj iteraciji. Fokus kursa ostaje na mehanizmima koji ovo omogućavaju (poput upravljanja memorijom i particionisanja), a ne na specifičnim ML modelima, tretirajući ove algoritme kao generalni Computer Science koncept koji koristi Spark-ovu in-memory paradigmu.

7. Vodič za ispit: Česta pitanja i mehanizmi oporavka

Za uspeh na ETH Zurich testovima iz Spark sekcije, neophodno je duboko razumevanje sledećih mehanizama:

Pitanje 1: Kako Spark postiže Fault Tolerance bez eksplicitne replikacije podataka?

* Odgovor: Spark koristi Lineage mehanizam unutar RDD-a. Umesto skupog čuvanja kopija podataka, sistem loguje sekvencu determinističkih transformacija koje su kreirale RDD. Pošto su podaci imutabilni, u slučaju otkaza čvora, Spark može rekonstruisati samo izgubljene particije ponovnim izvršavanjem transformacija na originalnom izvoru. Ovo je moguće isključivo zbog Lazy Evaluation principa koji omogućava sistemu da poznaje kompletan plan izvršavanja unapred.

Pitanje 2: Koja je uloga YARN-a u Spark ekosistemu i šta to znači za modularnost arhitekture?

* Odgovor: YARN (Yet Another Resource Negotiator) deluje kao univerzalni upravljač resursima na nivou klastera. Njegova uloga je da odvoji upravljanje resursima (CPU, RAM) od samog procesiranja podataka. Ovo omogućava Spark-u da koegzistira sa drugim endžinima (poput MapReduce-a ili Hive-a) na istom hardveru, što je ključna lekcija o evoluciji iz monolitnih "one-machine" stekova ka modernim modularnim cluster arhitekturama.

Pitanje 3: Analizirajte razliku između "narrow" i "wide" zavisnosti u kontekstu Stage Boundaries.

* Odgovor:
  * Narrow dependencies (Uske zavisnosti): Svaka particija roditelja se koristi od strane najviše jedne particije deteta (npr. map, filter). Ove operacije se izvršavaju unutar istog Stage-a i omogućavaju pipelining.
  * Wide dependencies (Široke zavisnosti): Zahtevaju da se podaci iz više particija roditelja redistribuiraju (shuffle) da bi se formirale particije deteta (npr. groupByKey, join).
  * Ispitni fokus: Široka zavisnost uvek definiše Stage Boundary (granicu faze). Spark mora da završi sve operacije pre shuffle-a i upiše podatke u lokalni shuffle-fajl pre nego što sledeći stage može da počne, što je najskuplja operacija u Spark-u.
