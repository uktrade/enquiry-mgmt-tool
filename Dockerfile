FROM python:3
ENV PYTHONUNBUFFERED 1
RUN export TERM=xterm-256color
RUN apt-get update
RUN apt-get install -y postgresql
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

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

COPY . /usr/src/app
