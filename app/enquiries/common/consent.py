from datetime import datetime

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests import HTTPError
from rest_framework import status

from app.enquiries.common.client import APIClient
from app.enquiries.common.hawk import HawkAuth

CONSENT_SERVICE_PATH_PERSON = "/api/v1/person/"


def request(url, method, **kwargs):
    if not all([
        settings.CONSENT_SERVICE_HAWK_ID,
        settings.CONSENT_SERVICE_HAWK_KEY,
        settings.CONSENT_SERVICE_BASE_URL,
    ]):
        raise ImproperlyConfigured("CONSENT_SERVICE_* environment variables must be set")

    client = APIClient(
        api_url=settings.CONSENT_SERVICE_BASE_URL,
        auth=HawkAuth(
            api_id=settings.CONSENT_SERVICE_HAWK_ID,
            api_key=settings.CONSENT_SERVICE_HAWK_KEY,
            verify_response=settings.CONSENT_SERVICE_VERIFY_RESPONSE,
        ),
        default_timeout=(
            settings.CONSENT_SERVICE_CONNECT_TIMEOUT,
            settings.CONSENT_SERVICE_READ_TIMEOUT,
        ),
    )
    return client.request(path=url, method=method, **kwargs)


def check_consent(key):
    if not settings.FEATURE_FLAGS["ENFORCE_CONSENT_SERVICE"]:
        return None

    key = key.lower().replace(" ", "")
    url = f"{settings.CONSENT_SERVICE_BASE_URL}{CONSENT_SERVICE_PATH_PERSON}{key}/"
    try:
        response = request(url=url, method="GET")
        return bool(len(response.json()["consents"]))
    except HTTPError as e:
        if e.response and e.response.status_code == status.HTTP_404_NOT_FOUND:
            return False
    return False


def set_consent(key, value=True):
    if not settings.FEATURE_FLAGS["ENFORCE_CONSENT_SERVICE"]:
        return None

    key = key.lower()
    key_type = "email" if "@" in key else "phone"

    data = {
        "consents": [f"{key_type}_marketing"] if value else [],
        key_type: key,
        "modified_at": datetime.now().isoformat(),
    }

    try:
        url = f"{settings.CONSENT_SERVICE_BASE_URL}{CONSENT_SERVICE_PATH_PERSON}"
        request(url=url, method="POST", json=data)
        return True
    except Exception:
        return None
