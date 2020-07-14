#!/bin/bash -xe

python manage.py migrate
sh setup-test-fixtures.sh
python manage.py runserver 0.0.0.0:8000