#!/bin/bash -xe

python manage.py migrate
sh setup-test-fixtures.sh
# -a to append coverage
exec coverage run -a manage.py runserver 0.0.0.0:8001
