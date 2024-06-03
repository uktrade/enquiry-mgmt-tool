#!/usr/bin/env bash

# Start-up script for the web process, primarily for GOV.UK PaaS (see the Procfile)

set  -xe

# Reset migrations for the enquiries app to zero
./manage.py migrate --fake enquiries zero

# Make migrations for the enquiries app
./manage.py makemigrations enquiries

# Apply migrations for the enquiries app
./manage.py migrate enquiries

# Apply migrations
./manage.py migrate --noinput

if [ -n "${COPILOT_ENVIRONMENT_NAME}" ]; then
  echo "Running in DBT Platform"
else
  echo "Running in Cloud Foundry"
  python manage.py collectstatic  --noinput
fi

gunicorn app.wsgi --config app/gunicorn.py
