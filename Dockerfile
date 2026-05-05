FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

USER root

RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list && \
    apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y python3 && \
    apt-get clean