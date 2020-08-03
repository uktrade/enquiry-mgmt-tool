"""
testfixtureapi_urls
-------------------

Setting `ROOT_URLCONF` to use this module instead of the default `urls.py`
will have the effect of adding the "Test Fixture API" URL(s) into the Django
URL router.

Obviously therefore this should never EVER be enabled in a live service
environment (this includes dev, staging, etc and OF COURSE production).

For information on how to set up and use this feature in testing, please
see the "Allowing for Fixture Reset during e2e tests" section of `README.md`.
"""
from app.urls import urlpatterns

from django.urls import include, path

urlpatterns.append(
    path('testfixtureapi/', include('app.testfixtureapi.urls')),
)
