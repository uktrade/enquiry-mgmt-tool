#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

# Add commands below to run inside the container after all the other buildpacks have been applied

export DJANGO_SECRET_KEY="build-time-secret"
export DEBUG="False"
export FEATURE_ENFORCE_STAFF_SSO_ENABLED="False"
export ACTIVITY_STREAM_ENQUIRY_POLL_INTERVAL_MINS="1"
export DATABASE_CREDENTIALS='{"username": "postgres", "password": "password", "engine": "postgres", "port": 5432, "dbname": "postgres", "host": "db", "dbInstanceIdentifier": "emt-db"}'


python manage.py collectstatic --noinput
