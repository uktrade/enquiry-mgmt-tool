#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

# Add commands below to run inside the container after all the other buildpacks have been applied

export DEBUG="True"
export DJANGO_SECRET_KEY="supersecretkey"

# Database settings
export DATABASE_CREDENTIALS='{"username": "postgres", "password": "password", "engine": "postgres", "port": 5432, "dbname": "postgres", "host": "db", "dbInstanceIdentifier": "emt-db"}'

# Sentry
export DJANGO_SENTRY_DSN=""

export ENQUIRIES_PER_PAGE="10"
export ENQUIRY_RESPONSIVENESS_PERIOD_WEEKS="6"

# DataHub links
export DATA_HUB_FRONTEND="https://www.datahub.dev.uktrade.io"
export DATA_HUB_CREATE_COMPANY_PAGE_URL="https://www.datahub.dev.uktrade.io/companies/create"

# DataHub API variables when running Data Hub API locally on port 8000
export DATA_HUB_METADATA_URL="http://docker.for.mac.localhost:8000/v4/metadsuf"
export DATA_HUB_COMPANY_SEARCH_URL="http://docker.for.mac.localhost:8000/v4/search/company"
export DATA_HUB_CONTACT_SEARCH_URL="http://docker.for.mac.localhost:8000/v3/search/contact"
export DATA_HUB_CONTACT_CREATE_URL="http://docker.for.mac.localhost:8000/v3/contact"
export DATA_HUB_INVESTMENT_CREATE_URL="http://docker.for.mac.localhost:8000/v3/investment"
export DATA_HUB_ADVISER_SEARCH_URL="http://docker.for.mac.localhost:8000/adviser/"
export DATA_HUB_WHOAMI_URL="http://docker.for.mac.localhost:8000/whoami/"

# Hawk
export DATA_HUB_ENQUIRY_MGMT_HAWK_ID="data-hub-enquiry-mgmt-hawk-id"
export DATA_HUB_ENQUIRY_MGMT_HAWK_SECRET_KEY="data-hub-enquiry-mgmt-hawk-secret-key"

# Celery and Redis
export ENQUIRY_STATUS_UPDATE_INTERVAL_DAYS="1"
export ENQUIRY_STATUS_SHOULD_UPDATE="0"
export REDIS_BASE_URL="redis://redis:6379"
export CELERY_TIMEZONE="UTC"

# Staff SSO/OAuth2 settings
export FEATURE_ENFORCE_STAFF_SSO_ENABLED="1"

# Control Consent Service
export FEATURE_ENFORCE_CONSENT_SERVICE="1"

# The AUTHBROKER_URL needs to be accessible from the browser for the
# authorization redirect and also from the Docker container for the access token
# POST request, and the only way to do this is to use the
# docker.for.mac.localhost host provided by Docker.
export AUTHBROKER_URL="http://docker.for.mac.localhost:8080"
export AUTHBROKER_CLIENT_ID="contact-web-ops-for-details"
export AUTHBROKER_CLIENT_SECRET="contact-web-ops-for-details"
export AUTHBROKER_TOKEN_SESSION_KEY="_authbroker_token"
export AUTHBROKER_STAFF_SSO_SCOPE="dummy-scope"

export MOCK_SSO_TOKEN="dummy-token"
export MOCK_SSO_SCOPE="dummy-scope"
export MOCK_SSO_USERNAME="testuser"
export MOCK_SSO_EMAIL_USER_ID="testuser@example.com"
export COMPOSE_PROJECT_NAME="enquiry-mgmt-tool"

# Deny http for the OAuth flow
export OAUTHLIB_INSECURE_TRANSPORT="0"

# Activity Stream
export ACTIVITY_STREAM_ENQUIRY_POLL_INTERVAL_MINS="1"
export ACTIVITY_STREAM_KEY_ID="enquiry-mgmt-key-id"
export ACTIVITY_STREAM_KEY="enquiry-mgmt-secret-key"
export ACTIVITY_STREAM_SEARCH_URL="https://activity-stream/search"
export ACTIVITY_STREAM_SEARCH_TARGET_URL="/international/invest/contact/"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY1="enquiry-key-1"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE1="enquiry-value-2"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2="enquiry-key-2"
export ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2="enquiry-value-2"
export ACTIVITY_STREAM_ENQUIRY_DATA_OBJ="enquiry-data-obj"

# Date from which enquiry data is to be fetched in AS
export ACTIVITY_STREAM_INITIAL_LOAD_DATE="01-January-2020"

# Settings for CSRF and Session cookies
export CSRF_COOKIE_SECURE="False"
export CSRF_COOKIE_HTTPONLY="False"
export SESSION_COOKIE_SECURE="False"
# SESSION_COOKIE_AGE=36000 # Optional, defaults to 32400 (9 hours)

# Set HSTS headers, only needs to be True in Production
export SET_HSTS_HEADERS="False"

export NON_RESPONSIVE_ENQUIRY_INITIAL_LOAD_DATE="01-April-2020"
export ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_NAME="enquiry-data-search-name"
export ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_VALUE="enquiry-data-search-value"

export ALLOW_TEST_FIXTURE_SETUP="allow"

echo "Running npm i"
npm i
echo "Running npm run sass"
npm run sass
echo "Running python manage.py collectstatic --noinput --traceback"
python manage.py collectstatic --noinput
