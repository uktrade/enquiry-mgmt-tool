from unittest import mock

import pytest

from app.enquiries import tasks


@mock.patch("app.enquiries.common.consent.set_consent")
@pytest.mark.parametrize("params", [
    ("KEY", True),
    ("KEY", False),
])
def test_update_enquirer_consents(mock_consent_set, params):
    key, value = params
    assert mock_consent_set.call_count == 0
    tasks.update_enquirer_consents.apply(kwargs={"key": key, "value": value})
    assert mock_consent_set.call_count == 1, (key, value)
