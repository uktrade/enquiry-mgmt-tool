#!/usr/bin/env bash

# Start-up script for the web process, primarily for GOV.UK PaaS (see the Procfile)

set  -xe

if [ -n "${COPILOT_ENVIRONMENT_NAME}" ]; then
  echo "Running in DBT Platform"
  ./manage.py migrate collectstatic --noinput
else
  echo "Running in Cloud Foundry"
  python manage.py collectstatic  --noinput
fi

gunicorn app.wsgi --config app/gunicorn.py
