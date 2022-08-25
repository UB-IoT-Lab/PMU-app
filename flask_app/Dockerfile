#FROM python:3.8-buster
FROM ubuntu:latest
WORKDIR /app

ADD . /app

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y lsof
#RUN pip install --upgrade pip
#RUN apt update


RUN pip install -r requirements.txt


CMD ["bash","test.sh"] //This is a script that is run when the container is started and it will run both flask and server.py
