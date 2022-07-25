FROM python:3.8-buster

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip
RUN apt update
RUN apt install net-tools

RUN pip install -r requirements.txt


CMD ["bash","test.sh"] //This is a script that is run when the container is started and it will run both flask and server.py
