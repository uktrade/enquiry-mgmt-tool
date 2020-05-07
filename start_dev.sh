#!/bin/bash -xe
export DJANGO_SETTINGS_MODULE=app.settings.dev
python manage.py migrate
python manage.py runserver 0.0.0.0:8000