"""
Django settings for enquiry_mgmt_tool project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import environ
import logging.config
import os
import sentry_sdk

from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from urllib.parse import urlencode

from django.urls import reverse_lazy

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
if not env.bool('DEBUG'):
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
}

# Application definition

INSTALLED_APPS = [
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
    INSTALLED_APPS.append("authbroker_client",)

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
    # MIDDLEWARE.append(
    #     # middleware to check auth for all views, alternatively use login_required decorator
    #     "authbroker_client.middleware.ProtectAllViewsMiddleware",
    # )
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
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
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

# App specific settings
CHAR_FIELD_MAX_LENGTH = 255
ENQUIRIES_PER_PAGE = env.int('ENQUIRIES_PER_PAGE', default=10)

# Data Hub settings
# TODO: Access token can be removed once SSO is integrated as it comes from SSO directly
DATA_HUB_ACCESS_TOKEN = env('DATA_HUB_ACCESS_TOKEN', default='dh-access-token')
DATA_HUB_METADATA_URL = env('DATA_HUB_METADATA_URL')
DATA_HUB_COMPANY_SEARCH_URL = env('DATA_HUB_COMPANY_SEARCH_URL')
DATA_HUB_CONTACT_SEARCH_URL = env('DATA_HUB_CONTACT_SEARCH_URL')

DATA_HUB_HAWK_ID = env("DATA_HUB_HAWK_ID")
DATA_HUB_HAWK_KEY = env("DATA_HUB_HAWK_KEY")

# Celery and Redis
CACHES = {}
DATA_HUB_METADATA_FETCH_INTERVAL_HOURS=env.int('DATA_HUB_METADATA_FETCH_INTERVAL_HOURS', default=4)
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
