from unittest import mock
from unittest.mock import patch

import pytest
from django.db import DatabaseError
from django.db.utils import OperationalError

from rest_framework import status
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


class ServiceHealthCheckTestCase():
    def test_all_good(self, client):
        """Test all good."""
        url = reverse('ping')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert '<status>OK</status>' in str(response.content)
        assert response.headers['content-type'] == 'text/xml'

    @mock.patch("app.enquiries.models.Enquiry.objects")
    def test_check_database_fail(self, client, model_manager):
        url = reverse('ping')
        with patch(
            'datahub.ping.services.Company.objects.all',
            side_effect=DatabaseError('No database'),
        ):
            model_manager.exists.side_effect = OperationalError("connection failure")

            response = client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert '<status>FALSE</status>' in str(response.content)
            assert response.headers['content-type'] == 'text/xml'
