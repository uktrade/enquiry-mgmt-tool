from app.settings.common import *

FEATURE_FLAGS = {
    "ENFORCE_STAFF_SSO_ON": True,
}

REST_FRAMEWORK["PAGE_SIZE"] = 2

CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
}
