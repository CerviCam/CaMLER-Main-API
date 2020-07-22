FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
MAINTAINER CerviCam

RUN mkdir /app
ADD apps /app/apps
ADD cervicam /app/cervicam
ADD manage.py /app/manage.py
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

RUN adduser -D tempuser
USER tempuser