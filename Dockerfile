
FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y sudo vim tmux python3 pip python3.10-venv libmagic1\
    && useradd -m alvgomez \
    && echo 'root:hola1' | chpasswd \
    && echo 'alvgomez:hola2' | chpasswd 

RUN mkdir /monitor_folder \
    && mkdir /var/log/irondome 

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

