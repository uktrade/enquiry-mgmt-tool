import requests
from cachecontrol import CacheControl
from cachecontrol_django import DjangoCache


cached_requests = CacheControl(
    requests.session(),
    cache=DjangoCache(),
)
