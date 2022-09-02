from unittest import mock
from requests import HTTPError

import pytest
from django.core.exceptions import ImproperlyConfigured

from app.enquiries.common import consent


class TestConsent:
    def set_valid_settings(self, settings):
        settings.FEATURE_FLAGS["ENFORCE_CONSENT_SERVICE"] = True
        settings.CONSENT_SERVICE_HAWK_ID = "id"
        settings.CONSENT_SERVICE_HAWK_KEY = "key"
        settings.CONSENT_SERVICE_BASE_URL = "http://local.host"
        settings.CONSENT_SERVICE_VERIFY_RESPONSE = False

    def test_is_disabled(self):
        assert consent.check_consent("key") is None
        assert consent.set_consent("key") is None

    def test_invalid_configuration(self, settings):
        settings.FEATURE_FLAGS["ENFORCE_CONSENT_SERVICE"] = True
        with pytest.raises(ImproperlyConfigured):
            consent.check_consent("key")

    @mock.patch('app.enquiries.common.consent.APIClient')
    def test_valid_configuration(self, mock_client, settings):
        self.set_valid_settings(settings)
        assert mock_client.call_count == 0
        consent.check_consent("key")
        assert mock_client.call_count == 1

    @pytest.mark.parametrize("params", [
        ("key", "key", "", False),
        ("key", "key", [], False),
        ("key", "key", ["aaa"], True),
        ("key", "key", ["aaa", "bbb"], True),
        ("KEY", "key", ["aaa", "bbb"], True),
        ("KEY 1 2", "key12", ["aaa", "bbb"], True),
    ])
    def test_check_consent(self, requests_mock, settings, params):
        key, path, consents, result = params
        self.set_valid_settings(settings)

        url = f"{settings.CONSENT_SERVICE_BASE_URL}/api/v1/person/{path}/"
        requests_mock.get(url=url, json={"consents": consents})
        assert consent.check_consent(key) is result

    def test_check_consent_when_404(self, requests_mock, settings):
        self.set_valid_settings(settings)

        url = f"{settings.CONSENT_SERVICE_BASE_URL}/api/v1/person/key/"
        requests_mock.get(url=url, status_code=404)
        assert consent.check_consent('key') is False

    def test_check_consent_when_500(self, requests_mock, settings):
        self.set_valid_settings(settings)

        url = f"{settings.CONSENT_SERVICE_BASE_URL}/api/v1/person/key/"
        requests_mock.get(url=url, status_code=500)
        with pytest.raises(HTTPError):
            consent.check_consent('key')

    @mock.patch('app.enquiries.common.consent.request')
    @pytest.mark.parametrize("params", [
        ("key", True, True),
        ("key", False, True),
    ])
    def test_set_consent_ok(self, request, settings, params):
        key, value, result = params
        settings.FEATURE_FLAGS["ENFORCE_CONSENT_SERVICE"] = True
        assert consent.set_consent(key, value) is result, (key, value, result)

    @mock.patch('app.enquiries.common.consent.request')
    @pytest.mark.parametrize("params", [
        ("key", True, None),
        ("key", False, None),
    ])
    def test_set_consent_error(self, request, settings, params):
        key, value, result = params
        settings.FEATURE_FLAGS["ENFORCE_CONSENT_SERVICE"] = True
        request.side_effect = Exception
        assert consent.set_consent(key, value) is result, (key, value, result)
