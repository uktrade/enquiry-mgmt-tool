#!/bin/bash -xe

python manage.py loaddata app/enquiries/fixtures/users.json
python manage.py loaddata app/enquiries/fixtures/enquiries.json
python manage.py createsuperuser --no-input