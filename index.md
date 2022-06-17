## BDEA Abgabe 3
### Twitter-Mock on Cassandra with Lucene

### Aufgabenstellung: Wir zwitschern uns einen!
Lassen Sie uns unser eigenes **Social Network** aufbauen. Damit es realistisch wird, stelle ich Ihnen unten einige (aus Twitter extrahierte Follower-Beziehungen zur Verfügung (der Original-Link existiert leider nicht mehr)) sowie einige Posts von Prominenten, die Sie bspw. zufällig auf die 100 User IDs mit den meisten Followern verteilen (vgl. Abfragen). Ferner soll das System das Speichern von Likes für Posts unterstützen (also von welchem User wurde ein Post eines anderen Users gelikt), diese generieren Sie bitte zufällig an passender Stelle.

Folgende Abfragen soll das System unterstützen:

1. Auflisten der Posts, die von einem Account gemacht wurden, bzw. ihm zugeordnet wurden
2. Finden der 100 Accounts mit den meisten Followern
3. Finden der 100 Accounts, die den meisten der Accounts folgen, die in 1) gefunden wurden
4. Auflisten der Informationen für die persönliche Startseite eines beliebigen Accounts (am besten mit den in 2) gefundenen Accounts ausprobieren); die Startseite soll Folgendes beinhalten (als getrennte Queries umsetzen):
- die Anzahl der Follower
- die Anzahl der verfolgten Accounts
- wahlweise die 25 neusten oder die 25 beliebtesten Posts der verfolgten Accounts (per DB-Abfrage)
5. Caching der Posts für die Startseite (vgl. 4), erfordert einen sog. Fan-Out in den Cache jedes Followers beim Schreiben eines neuen Posts 
6. Auflisten der 25 beliebtesten Posts, die ein geg. Wort enthalten (falls möglich auch mit UND-Verknüpfung mehrerer Worte)

### Beschreibung des methodischen Vorgehens
> Einfügen

### Probleme in der Umsetzung einer Twitter-Datenhaltung in Cassandra mit Lucene Plugin
> Einfügen

## Lessons Learned
> Einfügen
