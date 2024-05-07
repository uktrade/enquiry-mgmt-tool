#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

# Add commands below to run inside the container after all the other buildpacks have been applied

export DJANGO_SECRET_KEY="build-time-secret"
export DEBUG="False"
export FEATURE_ENFORCE_STAFF_SSO_ENABLED="False"

python manage.py collectstatic --noinput
