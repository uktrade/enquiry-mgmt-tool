from app.settings import *

REST_FRAMEWORK["PAGE_SIZE"] = 2

CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
}
