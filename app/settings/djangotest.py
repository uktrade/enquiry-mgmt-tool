from app.settings.common import *

ROOT_URLCONF = 'app.testfixtureapi_urls'

FEATURE_FLAGS = {
    "ENFORCE_STAFF_SSO_ON": True,
    "ENFORCE_CONSENT_SERVICE": False,
}

REST_FRAMEWORK["PAGE_SIZE"] = 10

CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
}


ACTIVITY_STREAM_ENQUIRY_DATA_OBJ = 'submission_data'
