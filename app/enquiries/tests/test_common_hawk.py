import re
from unittest.mock import Mock

import pytest
from freezegun import freeze_time

from app.enquiries.common.hawk import HawkAuth

BASE = "http://local.host/"


class TestHawkAuth:
    """Tests HawkAuth."""

    @freeze_time("2018-01-01 00:00:00")
    def test_requests_with_no_body_are_signed(self):
        """Tests that requests without a body are signed."""
        auth = HawkAuth("test-id", "test-key")
        request = Mock(method="GET", url=f"{BASE}test", body=None, headers={})
        auth(request)

        pattern = re.compile('Hawk mac=".*", hash=".*", id="test-id", ts="1514764800", nonce=".*"')
        assert pattern.match(request.headers["Authorization"])

    def test_exception_raised_if_response_fails_verification(self, monkeypatch):
        """Test that responses are verified when response verification is enabled."""
        accept_response_mock = Mock(side_effect=ValueError())
        monkeypatch.setattr("mohawk.Sender.accept_response", accept_response_mock)

        auth = HawkAuth("test-id", "test-key")
        request = Mock(method="GET", url=f"{BASE}test", body=None, headers={})
        auth(request)

        request.register_hook.assert_called_once()
        response = Mock(
            content=b"",
            ok=True,
            headers={
                "Server-Authorization": "test",
                "Content-Type": "test/test",
            },
        )

        with pytest.raises(ValueError):
            request.register_hook.call_args[0][1](response)

    def test_response_not_verified_if_verification_disabled(self):
        """Test that responses are not verified when response verification is disabled."""
        auth = HawkAuth("test-id", "test-key", verify_response=False)
        request = Mock(method="GET", url=f"{BASE}test", body=None, headers={})
        auth(request)

        request.register_hook.assert_not_called()
