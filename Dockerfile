FROM python:3

ENV PYTHONUNBUFFERED 1
ENV TERM xterm-256color

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Install NodeJS
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - \
    && apt-get install -y nodejs

# Install yarn
RUN npm install -g yarn@1.16.0

# Install Chrome browser
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y dbus-x11 google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Cypress
RUN apt-get update \
    && apt-get install -y libgtk2.0-0 libgtk-3-0 libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb \
    && yarn global add cypress

# Check version
RUN cypress -v \
    && node -v

# Install dockerize https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION v0.2.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Install PIP packages
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app
