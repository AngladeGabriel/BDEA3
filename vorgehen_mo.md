# BDEA - Abgabe 3

## Datenmodellierung


## Anleitung
### Data Folder anlegen im C* Container
- docker exec -it cass1 bash
- mkdir data

### CSVs in Container kopieren
- cd Documents/UNI/BDEA/CA_3/BDEA3/
- docker cp res_follower.csv cass1:/data/res_follower.csv
- docker cp tweets_clean.csv cass1:/data/tweets_clean.csv

### Aufsetzen der Tabellen

- docker exec -it cass1 cqlsh
- CREATE KEYSPACE twitter WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};
- USE twitter;
- CREATE TABLE twitter.tweets_by_authors (author TEXT, date_time TIMESTAMP, tweet_id BIGINT, content TEXT, language TEXT, number_of_likes INT, number_of_shares INT, PRIMARY KEY ((author), date_time, tweet_id)) WITH CLUSTERING ORDER BY (date_time DESC);
- CREATE TABLE twitter.follower_relations_by_users (username text, rel_type text, rel_target_id BIGINT, rel_target_username text,  PRIMARY KEY ((username), rel_type, rel_target_id));

### Follower Relations anlegen
- COPY twitter.follower_relations_by_users (username, rel_type, rel_target_username, rel_target_id) FROM 'data/res_follower.csv' WITH HEADER = TRUE;
- Testen, ob die Daten richtig importiert wurden:
  - SELECT COUNT(*) FROM twitter.follower_relations_by_users WHERE username = 'katyperry';

### Tweets anlegen
- COPY twitter.tweets_by_authors (author, content, date_time, tweet_id, language, number_of_likes, number_of_shares) FROM 'data/tweets_clean.csv' WITH HEADER = TRUE;
- Testen, ob die Daten richtig importiert wurden:
  - SELECT COUNT(*) FROM twitter.tweets_by_authors;

## Queries absetzen
1. **SELECT \* FROM twitter.tweets_by_authors WHERE author = 'katyperry';**</br></br>
2. SELECT username, COUNT(\*) AS followers FROM twitter.follower_relations_by_users WHERE rel_type = 'follower' GROUP BY username ALLOW FILTERING;</br>-> Extraktion der Top 100 per Skript und Schreiben in Time-Series-Table</br>-> Abfrage dann auf dieser Table</br></br>
3. tbd</br></br>
4. 
   1. **SELECT username, COUNT(\*) AS followers FROM twitter.follower_relations_by_users WHERE username = 'katyperry' AND rel_type = 'follower';**</br></br>
   2. **SELECT username, COUNT(\*) AS follows FROM twitter.follower_relations_by_users WHERE username = 'katyperry' AND rel_type = 'follows';**</br></br>
   3. SELECT * FROM twitter.caches_by_users WHERE username = 'katyperry' LIMIT 25;</br></br>
5. tbd</br></br>
6. SELECT \* FROM twitter.tweets_by_author WHERE expr (filter: [{filter_expression}] query: [{query_expression}] sort: [{sort_expression}]) LIMIT 25;

## Learnings
- Problematisch mit limitierten Ressourcen
- 2 GB RAM pro Node reichen hier nicht aus
- Mit 4 GB klappt es (grade so?)
- Für cassandra in prod Verhältnissen wird z-b 8GB empfohlen als Minimum