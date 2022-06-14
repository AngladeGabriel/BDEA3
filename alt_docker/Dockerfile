FROM ubuntu:16.04

#MAINTAINER Eranga Bandara (erangaeb@gmail.com)
LABEL class="BDEA"
LABEL abgabe="Abgabe3"
LABEL author="Gabriel Anglade"

# explicitly set user/group IDs
RUN groupadd -r cassandra --gid=999 && useradd -r -g cassandra --uid=999 cassandra

# install required packages
RUN apt-get update -y
RUN apt-get install -y python-software-properties
RUN apt-get install -y software-properties-common

# install java
# RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
# #RUN add-apt-repository -y ppa:webupd8team/java
# RUN add-apt-repository -y ppa:linuxuprising/java
# RUN apt-get update -y
# #RUN apt-get install -y oracle-java8-installer
# RUN apt-get install -y oracle-java11-installer
# RUN rm -rf /var/lib/apt/lists/*
# RUN rm -rf /var/cache/oracle-jdk11-installer
#RUN rm -rf /var/cache/oracle-jdk8-installer
#
# set JAVA_HOME
# ENV JAVA_HOME /usr/lib/jvm/java-11-oracle
#As paulscott56 said, you can add those lines in your Dockerfile:

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install default-jdk-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/



# install curl
RUN apt-get update && apt-get install -y curl

# install cassandra
# ENV MIRROR http://apache.mirrors.pair.com/
# ENV VERSION 3.11.0
# RUN curl $MIRROR/cassandra/$VERSION/apache-cassandra-$VERSION-bin.tar.gz | tar -xzf - -C /opt \
#     && mv /opt/apache-cassandra-$VERSION /opt/cassandra \
#     && mkdir -p /tmp/cassandra

ENV ARCHIVEMIRROR https://archive.apache.org/dist/cassandra
ENV VERSION 3.11.0
#maybe dont download src pkg lol
#RUN curl $ARCHIVEMIRROR/$VERSION/apache-cassandra-$VERSION-src.tar.gz   | tar -xzf - -C /opt \
RUN curl $ARCHIVEMIRROR/$VERSION/apache-cassandra-$VERSION-bin.tar.gz   | tar -xzf - -C /opt \
    && ls /opt \
    && mv /opt/apache-cassandra-$VERSION /opt/cassandra \
    && mkdir -p /tmp/cassandra

# install lucene plugin
ENV PLUGIN_VERSION 3.11.0.0
#RUN curl -LO http://search.maven.org/remotecontent\?filepath\=com/stratio/cassandra/cassandra-lucene-index-plugin/3.11.0.0/cassandra-lucene-index-plugin-3.11.0.0.jar
RUN curl -LO https://repo1.maven.org/maven2/com/stratio/cassandra/cassandra-lucene-index-plugin/3.11.0.0/cassandra-lucene-index-plugin-3.11.0.0.jar 
RUN mv cassandra-lucene-index-plugin-3.11.0.0.jar /opt/cassandra/lib

# post installation config
ADD configure.sh /opt/cassandra
RUN chmod +x /opt/cassandra/configure.sh
ENTRYPOINT ["/opt/cassandra/configure.sh"]

RUN chown -R cassandra:cassandra /opt/cassandra

# start
USER cassandra
WORKDIR /opt/cassandra

# 7000: ipc; 7001: tls ipc; 7199: jmx; 9042: cql; 9160: thrift
EXPOSE 7000 7001 7199 9042 9160

CMD ["/opt/cassandra/bin/cassandra", "-f"]