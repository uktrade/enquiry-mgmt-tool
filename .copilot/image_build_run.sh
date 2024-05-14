#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

# Add commands below to run inside the container after all the other buildpacks have been applied

export DJANGO_SECRET_KEY="build-time-secret"
export DEBUG="False"
export FEATURE_ENFORCE_STAFF_SSO_ENABLED="False"
export ACTIVITY_STREAM_ENQUIRY_POLL_INTERVAL_MINS="1"
export DATABASE_CREDENTIALS='{"username": "postgres", "password": "password", "engine": "postgres", "port": 5432, "dbname": "postgres", "host": "db", "dbInstanceIdentifier": "emt-db"}'
export DATA_HUB_METADATA_URL="http://docker.for.mac.localhost:8000/v4/metadsuf"
export DATA_HUB_COMPANY_SEARCH_URL="http://docker.for.mac.localhost:8000/v4/search/company"
export DATA_HUB_CONTACT_SEARCH_URL="http://docker.for.mac.localhost:8000/v3/search/contact"
export DATA_HUB_CONTACT_CREATE_URL="http://docker.for.mac.localhost:8000/v3/contact"
export DATA_HUB_INVESTMENT_CREATE_URL="http://docker.for.mac.localhost:8000/v3/investment"
export DATA_HUB_ADVISER_SEARCH_URL="http://docker.for.mac.localhost:8000/adviser/"
export DATA_HUB_WHOAMI_URL="http://docker.for.mac.localhost:8000/whoami/"
export DATA_HUB_FRONTEND="https://www.datahub.dev.uktrade.io"
export DATA_HUB_CREATE_COMPANY_PAGE_URL="https://www.datahub.dev.uktrade.io/companies/create"
export DATA_HUB_HAWK_ID="hawk-id"
export DATA_HUB_HAWK_KEY="hawk-key"

export ACTIVITY_STREAM_ENQUIRY_POLL_INTERVAL_MINS="1"
export ACTIVITY_STREAM_KEY_ID="enquiry-mgmt-key-id"
export ACTIVITY_STREAM_KEY="enquiry-mgmt-secret-key"
export ACTIVITY_STREAM_INITIAL_LOAD_DATE="01-January-2020"
export ACTIVITY_STREAM_SEARCH_URL="https://activity-stream/search"
export ACTIVITY_STREAM_SEARCH_TARGET_URL="/international/invest/contact/"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY1="enquiry-key-1"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE1="enquiry-value-2"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2="enquiry-key-2"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2="enquiry-value-2"
export ACTIVITY_STREAM_ENQUIRY_DATA_OBJ="enquiry-data-obj"
export NON_RESPONSIVE_ENQUIRY_INITIAL_LOAD_DATE="01-April-2020"
export ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_NAME="enquiry-data-search-name"
export ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_VALUE="enquiry-data-search-value"

python manage.py collectstatic --noinput
