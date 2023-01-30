FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src /src
COPY ./requirements.txt requirements.txt

WORKDIR /automation

EXPOSE 8000

RUN pip install -r requirements.txt

