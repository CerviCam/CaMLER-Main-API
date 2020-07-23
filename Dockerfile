FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ADD apps /app/apps
ADD cervicam /app/cervicam
ADD manage.py /app/manage.py
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt