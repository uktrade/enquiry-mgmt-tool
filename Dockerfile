FROM python:3
ENV PYTHONUNBUFFERED 1
RUN export TERM=xterm-256color
RUN apt-get update
RUN apt-get install -y postgresql
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY . /usr/src/app
