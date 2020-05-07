from app.settings.common import *

ROOT_URLCONF = 'app.test_urls'

FEATURE_FLAGS = {
    "ENFORCE_STAFF_SSO_ON": True,
}

if env('ALLOW_TEST_FIXTURE_API_URLS', default=None) == 'allow':
    # For obvious reasons, never EVER set this to True in non-test environments
    ALLOW_TEST_FIXTURE_API_URLS = True
else:
    ALLOW_TEST_FIXTURE_API_URLS = False

REST_FRAMEWORK["PAGE_SIZE"] = 2

CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
}


ACTIVITY_STREAM_ENQUIRY_DATA_OBJ = 'submission_data'
