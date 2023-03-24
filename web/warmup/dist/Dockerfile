# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY . .
RUN pip3 install -r requirements.txt


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
