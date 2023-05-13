
FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y sudo vim tmux python3 \
    && useradd -m alvgomez \
    && echo 'root:hola' | chpasswd 

RUN mkdir /irondome \
    && mkdir monitor_folder \
    && mkdir /var/log/irondome

WORKDIR /irondome

COPY ./irondome /irondome/irondome

