"""
Django settings for enquiry_mgmt_tool project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import logging.config
import os
from urllib.parse import urlencode

import environ
import sentry_sdk
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.utils import timezone
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

environ.Env.read_env()  # read the .env file which should be in the same folder as settings.py
env = environ.Env()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] [%(levelname)-4s] %(name)-8s: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG' if env.bool('DEBUG') else 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
})

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure Sentry
DJANGO_SENTRY_DSN = env('DJANGO_SENTRY_DSN')
sentry_sdk.init(
    dsn=DJANGO_SENTRY_DSN,
    integrations=[
        CeleryIntegration(),
        DjangoIntegration(),
    ],
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

# As app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

FEATURE_FLAGS = {
    "ENFORCE_STAFF_SSO_ON": env.bool("FEATURE_ENFORCE_STAFF_SSO_ENABLED", True),
    "ENFORCE_CONSENT_SERVICE": env.bool("FEATURE_ENFORCE_CONSENT_SERVICE", True),
}

# Application definition

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "widget_tweaks",
    "app.enquiries",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'app.middleware.add_cache_control_header_middleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': env.int('ENQUIRIES_PER_PAGE', default=10),
}

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

AUTH_USER_MODEL = "enquiries.Owner"

# authbroker config
if FEATURE_FLAGS["ENFORCE_STAFF_SSO_ON"]:
    TEST_SSO_PROVIDER_SET_RETURNED_ACCESS_TOKEN = env("MOCK_SSO_TOKEN", default=None)
    INSTALLED_APPS.append("authbroker_client", )

    AUTHBROKER_URL = env("AUTHBROKER_URL")
    AUTHBROKER_CLIENT_ID = env("AUTHBROKER_CLIENT_ID")
    AUTHBROKER_CLIENT_SECRET = env("AUTHBROKER_CLIENT_SECRET")
    AUTHBROKER_TOKEN_SESSION_KEY = env("AUTHBROKER_TOKEN_SESSION_KEY")
    AUTHBROKER_STAFF_SSO_SCOPE = env('AUTHBROKER_STAFF_SSO_SCOPE')
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "authbroker_client.backends.AuthbrokerBackend",
    ]

    LOGIN_URL = reverse_lazy("authbroker_client:login")
    LOGIN_REDIRECT_URL = reverse_lazy("index")
else:
    LOGIN_URL = "/admin/login/"
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        **env.db('DATABASE_URL'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(APP_ROOT, 'enquiries', 'static')
STATICFILES_DIRS = [
    ('govuk-frontend', 'node_modules/govuk-frontend/govuk'),
]

# This setting alone will NOT enable the "Test Fixture API" facility -
# By default the URL to it is not enabled. See README.md section
# "Allowing for Fixture Reset during e2e tests" for details how to
# enable the URL and turn on the Test Fixture API.
ALLOW_TEST_FIXTURE_SETUP = env('ALLOW_TEST_FIXTURE_SETUP', default=None) == 'allow'

# Set security related headers
SET_HSTS_HEADERS = env('SET_HSTS_HEADERS', default=True)
if SET_HSTS_HEADERS:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_BROWSER_XSS_FILTER = True

# App specific settings
CHAR_FIELD_MAX_LENGTH = 255
ENQUIRIES_PER_PAGE = env.int('ENQUIRIES_PER_PAGE', default=10)
ENQUIRIES_PAGE_SIZE_PARAM = env.int('ENQUIRIES_PAGE_SIZE_PARAM', default='page_size')
ENQUIRY_RESPONSIVENESS_PERIOD_WEEKS = env.int('ENQUIRY_RESPONSIVENESS_PERIOD_WEEKS', default=6)
ENQUIRY_SORT_OPTIONS = {
    "company_name": "Company name: A-Z",
    "-modified": "Most recently updated",
    "date_received": "Least recently received",
}
IMPORT_ENQUIRIES_MIME_TYPES = ["text/csv", "application/vnd.ms-excel"]
IMPORT_TEMPLATE_FILENAME = 'rtt_enquiries_import_template.xlsx'
IMPORT_TEMPLATE_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
UPLOAD_CHUNK_SIZE = 256000
EXPORT_OUTPUT_FILE_SLUG = 'rtt_enquiries_export'
EXPORT_OUTPUT_FILE_EXT = 'csv'
EXPORT_OUTPUT_FILE_MIMETYPE = 'text/csv'
EXPORT_OUTPUT_FILE_CSV_HEADERS = [
        'client_relationship_manager', 'company_name', 'country', 'created',
        'date_added_to_datahub', 'date_received', 'enquirer.email',
        'enquirer.first_name', 'enquirer.job_title',
        'enquirer.last_name', 'enquirer.phone',
        'enquirer.phone_country_code', 'enquirer.request_for_call', 'enquiry_stage',
        'enquiry_text', 'estimated_land_date', 'first_hpo_selection', 'first_response_channel',
        'google_campaign', 'how_they_heard_dit', 'investment_readiness', 'investment_type',
        'ist_sector', 'marketing_channel', 'notes', 'owner', 'owner.first_name', 'owner.last_name',
        'primary_sector', 'project_code', 'project_name', 'project_success_date', 'quality',
        'region', 'second_hpo_selection', 'third_hpo_selection', 'website']

# Data Hub settings
DATA_HUB_METADATA_URL = env('DATA_HUB_METADATA_URL')
DATA_HUB_COMPANY_SEARCH_URL = env('DATA_HUB_COMPANY_SEARCH_URL')
DATA_HUB_CONTACT_SEARCH_URL = env('DATA_HUB_CONTACT_SEARCH_URL')
DATA_HUB_CONTACT_CREATE_URL = env('DATA_HUB_CONTACT_CREATE_URL')
DATA_HUB_ADVISER_SEARCH_URL = env('DATA_HUB_ADVISER_SEARCH_URL')
DATA_HUB_INVESTMENT_CREATE_URL = env('DATA_HUB_INVESTMENT_CREATE_URL')
DATA_HUB_WHOAMI_URL = env('DATA_HUB_WHOAMI_URL')
DATA_HUB_FRONTEND = env('DATA_HUB_FRONTEND')
DATA_HUB_CREATE_COMPANY_PAGE_URL = env('DATA_HUB_CREATE_COMPANY_PAGE_URL')

DATA_HUB_HAWK_ID = env("DATA_HUB_HAWK_ID")
DATA_HUB_HAWK_KEY = env("DATA_HUB_HAWK_KEY")

# Celery and Redis
CACHES = {}
VCAP_SERVICES = env.json('VCAP_SERVICES', default={})

if 'redis' in VCAP_SERVICES:
    REDIS_BASE_URL = VCAP_SERVICES['redis'][0]['credentials']['uri']
else:
    REDIS_BASE_URL = env('REDIS_BASE_URL', default=None)

if REDIS_BASE_URL:
    REDIS_CACHE_DB = env('REDIS_CACHE_DB', default=0)
    REDIS_CELERY_DB = env('REDIS_CELERY_DB', default=1)
    is_secure_redis = REDIS_BASE_URL.startswith('rediss://')
    redis_url_args = {'ssl_cert_reqs': 'required'} if is_secure_redis else {}
    encoded_query_args = urlencode(redis_url_args)
    BROKER_URL = f'{REDIS_BASE_URL}/{REDIS_CELERY_DB}?{encoded_query_args}'
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_TIMEZONE = env('CELERY_TIMEZONE', default='Europe/london')
    ENQUIRY_STATUS_UPDATE_INTERVAL_DAYS = env.int('ENQUIRY_STATUS_UPDATE_INTERVAL_DAYS', default=1)
    ENQUIRY_STATUS_SHOULD_UPDATE = env.bool('ENQUIRY_STATUS_SHOULD_UPDATE', True)

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f'{REDIS_BASE_URL}/{REDIS_CACHE_DB}',
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
                "SOCKET_TIMEOUT": 5,  # in seconds
            }
        }
    }

# Activity stream settings
#
ACTIVITY_STREAM_ENQUIRY_POLL_INTERVAL_MINS = env('ACTIVITY_STREAM_ENQUIRY_POLL_INTERVAL_MINS', default=30)
ACTIVITY_STREAM_KEY_ID = env('ACTIVITY_STREAM_KEY_ID')
ACTIVITY_STREAM_KEY = env('ACTIVITY_STREAM_KEY')
# Date from which we want to pull the enquiries data
ACTIVITY_STREAM_INITIAL_LOAD_DATE = env('ACTIVITY_STREAM_INITIAL_LOAD_DATE')
ACTIVITY_STREAM_SEARCH_URL = env('ACTIVITY_STREAM_SEARCH_URL')
# search url for additional filtering as it is not part of the fields mapped for searching
ACTIVITY_STREAM_SEARCH_TARGET_URL = env('ACTIVITY_STREAM_SEARCH_TARGET_URL')
# Fields required to retrieve the relevant object in the search results
# retrieved data is a list of nested objects and these fields allow us
# to extract enquiry data and some assocoated metadata
ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY1 = env('ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY1')
ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE1 = env('ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE1')
ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2 = env('ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2')
ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2 = env('ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2')
# key of the object that contains enquiry data
ACTIVITY_STREAM_ENQUIRY_DATA_OBJ = env('ACTIVITY_STREAM_ENQUIRY_DATA_OBJ')

# Settings for CSRF and Session cookies
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', default=True)
CSRF_COOKIE_HTTPONLY = env('CSRF_COOKIE_HTTPONLY', default=True)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', default=True)
# Setting the session expiration to less than the expiration of the SSO access
# token (currently 10 hours) is the simplest way of keeping the token valid.
# It forces the user to go through the /auth/login endpoint just before the
# token expires which gets the user a fresh one.
SESSION_COOKIE_AGE = env("SESSION_COOKIE_AGE", default=60 * 60 * 9)

ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_NAME = env('ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_NAME')
ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_VALUE = env('ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_VALUE')

NON_RESPONSIVE_ENQUIRY_INITIAL_LOAD_DATE = env.str('NON_RESPONSIVE_ENQUIRY_INITIAL_LOAD_DATE', '01-February-2020')

CAMPAIGN_ENQUIRIES_POLL_INTERVAL_MINS = env.str('CAMPAIGN_ENQUIRIES_POLL_INTERVAL_MINS', 30)

AUTH_PAAS_IP_CHECK_DISABLE = env.bool('AUTH_PAAS_IP_CHECK_DISABLE', default=False)
AUTH_PAAS_IP_WHITELIST = env.list('AUTH_PAAS_IP_WHITELIST', default=[])
AUTH_PAAS_ADDED_X_FORWARDED_FOR_IPS = 2

# Legal Basis / Consent Service
CONSENT_SERVICE_BASE_URL = env('CONSENT_SERVICE_BASE_URL', default=None)
CONSENT_SERVICE_HAWK_ID = env('CONSENT_SERVICE_HAWK_ID', default=None)
CONSENT_SERVICE_HAWK_KEY = env('CONSENT_SERVICE_HAWK_KEY', default=None)
CONSENT_SERVICE_VERIFY_RESPONSE = env('CONSENT_SERVICE_VERIFY_RESPONSE', default=True)
CONSENT_SERVICE_CONNECT_TIMEOUT = env('CONSENT_SERVICE_CONNECT_TIMEOUT', default=5.0)
CONSENT_SERVICE_READ_TIMEOUT = env('CONSENT_SERVICE_READ_TIMEOUT', default=30.0)

# Hawk
HAWK_NONCE_EXPIRY_SECONDS = 60
HAWK_CREDENTIALS = {}


def _add_hawk_credentials(id_env_name, key_env_name, scopes):
    id_ = env(id_env_name, default=None)

    if not id_:
        return

    if id_ in HAWK_CREDENTIALS:
        raise ImproperlyConfigured(
            'Duplicate Hawk access key IDs detected. All access key IDs should be unique.',
        )

    HAWK_CREDENTIALS[id_] = {
        'key': env(key_env_name),
        'scopes': scopes,
    }


_add_hawk_credentials(
    'DATA_FLOW_HAWK_ID',
    'DATA_FLOW_HAWK_KEY',
    ('enquiries',),
)
