# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ .
COPY solve/flag.txt flag.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]