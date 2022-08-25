#FROM python:3.8-buster

FROM ubuntu:18.04


#RUN apt update
#RUN apt install python3-pip

WORKDIR /app
ADD . /app
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN apt-get install -y python3-pip
#RUN  apt-get install software-properties-common
#RUN  add-apt-repository universe
#RUN apt-get update -y
#RUN apt-get install -y python3-pip
RUN apt-get install -y lsof
#RUN pip install --upgrade pip
#RUN apt update


RUN pip3 install -r requirements.txt


CMD ["bash","test.sh"] This is a script that is run when the container is started and it will run both flask and server.py
