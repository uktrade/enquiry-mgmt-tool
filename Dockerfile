FROM python:3.12

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV TERM xterm-256color

# Install dockerize https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
# If the above doesn't work on Apple M1 silicon chipset
# Error runtime: failed to create new OS thread (have 2 already; errno=22) fatal error: newosproc)  
# use:
# RUN wget https://github.com/powerman/dockerize/releases/download/v0.16.0/dockerize-linux-arm64 -O /usr/local/bin/dockerize && chmod a+x /usr/local/bin/dockerize


# Install PIP packages
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
