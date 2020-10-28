import pytest
from django.conf import settings
from django.core.cache import CacheHandler
from pytest_django.lazy_django import skip_if_no_django


@pytest.fixture
def api_client():
    """Django REST framework ApiClient instance."""
    skip_if_no_django()

    from rest_framework.test import APIClient
    return APIClient(SERVER_NAME="testserver")


@pytest.fixture()
def local_memory_cache(monkeypatch):
    """Configure settings.CACHES to use LocMemCache."""
    monkeypatch.setitem(
        settings.CACHES,
        'default',
        {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
    )
    cache_handler = CacheHandler()
    monkeypatch.setattr('django.core.cache.caches', cache_handler)

    yield

    cache_handler['default'].clear()
