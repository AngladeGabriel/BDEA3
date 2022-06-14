#!/bin/bash
CASSANDRA_HOME=/opt/cassandra
CASSANDRA_HOST="$(hostname --ip-address)"
CLUSTER_NAME="senzchain"
WRITE_TIME_OUT=20000

sed -ri 's/^(# )?('"cluster_name"':).*/\2 '"$CLUSTER_NAME"'/' "$CASSANDRA_HOME/conf/cassandra.yaml"
sed -ri 's/^(# )?('"listen_address"':).*/\2 '"$CASSANDRA_HOST"'/' "$CASSANDRA_HOME/conf/cassandra.yaml"
sed -ri 's/^(# )?('"rpc_address"':).*/\2 '"$CASSANDRA_HOST"'/' "$CASSANDRA_HOME/conf/cassandra.yaml"
sed -ri 's/^(# )?('"write_request_timeout_in_ms"':).*/\2 '"$WRITE_TIME_OUT"'/' "$CASSANDRA_HOME/conf/cassandra.yaml"

# config broadcast address
if [ -z "$CASSANDRA_BROADCAST_ADDRESS" ]; then
    CASSANDRA_BROADCAST_ADDRESS=$CASSANDRA_HOST
fi
sed -ri 's/^(# )?('"broadcast_address"':).*/\2 '"$CASSANDRA_BROADCAST_ADDRESS"'/' "$CASSANDRA_HOME/conf/cassandra.yaml"
sed -ri 's/^(# )?('"broadcast_rpc_address"':).*/\2 '"$CASSANDRA_BROADCAST_ADDRESS"'/' "$CASSANDRA_HOME/conf/cassandra.yaml"

# config cassandra seeds
if [ -z "$CASSANDRA_SEEDS" ]; then
	CASSANDRA_SEEDS=$CASSANDRA_BROADCAST_ADDRESS
fi
sed -ri 's/(- seeds:).*/\1 "'"$CASSANDRA_SEEDS"'"/' "$CASSANDRA_HOME/conf/cassandra.yaml"

exec "$@"