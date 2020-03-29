#!/usr/bin/env bash

# Start-up script for the web process, primarily for GOV.UK PaaS (see the Procfile)

set  -xe

# Compile css
npm rebuild node-sass && npm install && npm run sass

./manage.py migrate --noinput

gunicorn app.wsgi --config app/gunicorn.py
