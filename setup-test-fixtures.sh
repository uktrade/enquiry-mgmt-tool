#!/bin/bash -xe
python manage.py teardowndata
python manage.py loaddata app/enquiries/fixtures/test_users.json
python manage.py loaddata app/enquiries/fixtures/test_enquiries.json
python manage.py createsuperuser --no-input