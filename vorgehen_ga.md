# Vorgehen Abgabe 3

- Quelle: Setup Cassandra as dockerized Cluster
- [Quelle](https://blog.digitalis.io/containerized-cassandra-cluster-for-local-testing-60d24d70dcc4)
  
## Begründung Cassandra


## Step 1:
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
