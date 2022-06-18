FROM jeffharwell/cassandra-lucene:3.11.6.0v1
LABEL maintainer="Gabriel Anglade"
LABEL description="Thanks to Jeff Harwell for this image, but not for his stupid entrypoint-skript that made me waste 2 hours understanding why my yaml was being overwritten"
RUN rm -f /etc/cassandra/cassandra.yaml
COPY ./yml/etc/cassandra/cassandra.yaml /etc/cassandra/cassandra.yaml
RUN rm -f ./docker-entrypoint.sh
# set own skript
COPY ./docker-entry/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
COPY ./yml/etc/cassandra/cassandra.yaml /etc/cassandra/cassandra.yaml