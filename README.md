# BDEA - Abgabe 3

- Quelle: Setup Cassandra as dockerized Cluster
- [Quelle](https://blog.digitalis.io/containerized-cassandra-cluster-for-local-testing-60d24d70dcc4)

## Begründung Cassandra
tbd

## Datenmodellierung
tbd

![Data model](assets/data_model.svg)

## Setup Cassandra

- Pull des Docker Images
  ```docker image pull cassandra:3.11.8```
- Kopieren der Config Files von einem Wegwerf-Container
  ```bash
  cd <workfolder>
  docker run --rm -d --name tmp cassandra:3.11.8
  docker cp tmp:/etc/cassandra etc_cassandra-3.11.8_vanilla
  docker stop tmp
  ```
- Erstellen der docker-compose.yml
  Enthält cass1, cass2, cass3, siehe mitgelieferte docker-compose.yml

  Wichtig: Die yaml der Quelle enthält einen fehler
  Ersetzen von Zeile 70 mit ```condition: service_healthy # cass3 only after cass2```

- Kopieren der Config Files in node-spezifische dirs
  ```bash
  mkdir -p etc
  cp -a etc_cassandra-3.11.8_vanilla etc/cass1
  cp -a etc_cassandra-3.11.8_vanilla etc/cass2
  cp -a etc_cassandra-3.11.8_vanilla etc/cass3
  ```

- starten der docker-compose
  ```docker-compose up -d```
  warten bis das Starten der nodes fertig ist
  ```docker ps```  
  prüfen dass nodes korrekt hochgefahren
    - clusterstatus prüfen: ```docker exec cass1 nodetool status```
    - CQL Check: ```docker exec -it cass1 cqlsh -e "describe keyspaces"```
### Data Folder anlegen im C* Container
```bash
docker exec -it cass1 bash
mkdir data
```

### CSVs in Container kopieren
```bash
cd Documents/UNI/BDEA/CA_3/BDEA3/
docker cp res_follower.csv cass1:/data/res_follower.csv
docker cp tweets_clean.csv cass1:/data/tweets_clean.csv
```

### Aufsetzen der Tabellen
```bash
docker exec -it cass1 cqlsh
CREATE KEYSPACE twitter WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};
USE twitter;
CREATE TABLE twitter.tweets_by_authors (author TEXT, date_time TIMESTAMP, tweet_id BIGINT, content TEXT, language TEXT, number_of_likes INT, number_of_shares INT, PRIMARY KEY ((author), date_time, tweet_id)) WITH CLUSTERING ORDER BY (date_time DESC);
CREATE TABLE twitter.caches_by_users (username TEXT, date_time TIMESTAMP, tweet_id BIGINT, author TEXT, content TEXT, language TEXT, number_of_likes INT, number_of_shares INT, PRIMARY KEY ((username), date_time, tweet_id)) WITH CLUSTERING ORDER BY (date_time DESC);
CREATE TABLE twitter.follower_relations_by_users (username text, rel_type text, rel_target_id BIGINT, rel_target_username text,  PRIMARY KEY ((username), rel_type, rel_target_id));
```
### Tweets Index für Lucene anlegen
```bash
CREATE CUSTOM INDEX tweets_index ON twitter.tweets_by_authors () USING 'com.stratio.cassandra.lucene.Index' WITH OPTIONS = {'refresh_seconds': 1, 'schema': '{fields: {author: {type: "text", analyzer: "english"}, date_time: {type: "date", pattern: "yyyy-MM-dd HH:MM:SS"}, tweet_id: {type: "integer"}, content: {type: "string"}, language: {type: "string"}, number_of_likes: {type: "integer"}, number_of_shares: {type: "integer"}}}'};
```
### Follower Relations importieren
```bash
COPY twitter.follower_relations_by_users (username, rel_type, rel_target_username, rel_target_id) FROM 'data/res_follower.csv' WITH HEADER = TRUE;
```
Testen, ob die Daten erfolgreich importiert wurden
```bash
SELECT COUNT(*) FROM twitter.follower_relations_by_users WHERE username = 'katyperry';
```
### Tweets importieren
```bash
COPY twitter.tweets_by_authors (author, content, date_time, tweet_id, language, number_of_likes, number_of_shares) FROM 'data/tweets_clean.csv' WITH HEADER = TRUE;
```
Testen, ob die Daten erfolgreich importiert wurden:
```bash
SELECT COUNT(*) FROM twitter.tweets_by_authors;
```
## Queries absetzen
![Queries](assets/queries.png)
1. ```SELECT \* FROM twitter.tweets_by_authors WHERE author = 'katyperry';```</br></br>
2. ```SELECT username, COUNT(\*) AS followers FROM twitter.follower_relations_by_users WHERE rel_type = 'follower' GROUP BY username ALLOW FILTERING;```</br>
-> Extraktion der Top 100 per Skript und Schreiben in Time-Series-Table</br>
-> Abfrage dann auf dieser Table</br>
```SELECT follower_json FROM twitter.top100_accounts_by_time LIMIT 1;```</br></br>
3. tbd</br></br>
4. 
    1. ```SELECT username, COUNT(\*) AS followers FROM twitter.follower_relations_by_users WHERE username = 'katyperry' AND rel_type = 'follower';```</br></br>
    2. ```SELECT username, COUNT(\*) AS follows FROM twitter.follower_relations_by_users WHERE username = 'katyperry' AND rel_type = 'follows';```</br></br>
    3. Mit Python Skript **init_cache_for_user.py** den Cache für einen beliebigen User initialisieren. Danach mit folgender Abfrage die 25 neusten Post der verfolgten Accounts des jeweiligen Users aus dem Cache abrufen:</br>
   ```SELECT * FROM twitter.caches_by_users WHERE username = <username> LIMIT 25;```</br></br>
5. In C* leider nicht mit Queries alleine umsetzbar. Lösung daher mit Python Skript -> **insert_new_tweet.py**.</br>
- Neuen Tweet in twitter.tweets_by_authors schreiben
- Follower des Autors aus twitter.follower_relations_by_user extrahieren
- Neuen Tweet jeweils in den Cache jedes Followers in twitter.caches_by_users schreiben</br></br>
6. Eigentlich bietet Lucene hier die Filter-Types **phrase** und **contains** an, um nach den Vorkommnissen gewisser Keywords zu suchen. Leider gab es hierbei insoweit Probleme, dass unter Verwendung besagter Filter-Types ein **Equals** statt **Contains** abgebildet wurde. Da wir die Ursache des Problems nicht identifizieren konnten, haben wir hier stattdesssen die Filter-Types **wildcard** und **regexp** verwendet, um die gewünschte Funktionalität abzubilden.</br></br>
   Für einen Begriff:</br>
   ```SELECT * FROM twitter.tweets_by_authors WHERE expr(tweets_index, '{filter: {type: "wildcard", field: "content", value: "\*hello\*"}, sort: {field: "number_of_likes", reverse: true}}') LIMIT 25;```</br></br>
   Für zwei - x Begriffe:</br>
   ```SELECT * FROM twitter.tweets_by_authors WHERE expr(tweets_index, '{filter: {type: "regexp", field: "content", value: "(.\*\n\*from.\*\n\*hello.\*\n\*)|(.\*\n\*hello.\*\n\*from.\*\n\*)"}, sort: {field: "number_of_likes", reverse: true}}') LIMIT 25;```
## Learnings
- Problematisch mit limitierten Ressourcen
- 2 GB RAM pro Node reichen hier nicht aus
- Mit 4 GB klappt es (grade so?)
- Für C* in prod Verhältnissen wird z-b 8GB empfohlen als Minimum