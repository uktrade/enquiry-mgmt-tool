FROM python:3.8

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV TERM xterm-256color

# Install dockerize https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION v0.2.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
# Mac M1 chipset
#RUN wget https://github.com/powerman/dockerize/releases/download/v0.16.0/dockerize-linux-arm64 -O /usr/local/bin/dockerize && chmod a+x /usr/local/bin/dockerize

# Install PIP packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install PIP packages
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
