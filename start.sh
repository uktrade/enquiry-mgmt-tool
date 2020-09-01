#!/bin/bash -xe

python manage.py migrate
sh setup-test-fixtures.sh
exec coverage run manage.py runserver 0.0.0.0:8001 --noreload