#!/usr/bin/env bash

# Start-up script for the web process, primarily for GOV.UK PaaS (see the Procfile)

set  -xe

./manage.py migrate --noinput
./manage.py collectstatic --noinput

gunicorn app.wsgi --config app/gunicorn.py
