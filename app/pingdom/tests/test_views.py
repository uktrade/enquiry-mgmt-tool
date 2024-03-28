import pytest
from unittest.mock import patch

from app.enquiries.tests import test_dh_utils
from django.db import DatabaseError

from rest_framework import status
from rest_framework.reverse import reverse
from redis.exceptions import RedisError

pytestmark = pytest.mark.django_db


class ServiceHealthCheckPingdomTestCase(test_dh_utils.DataHubUtilsTests):
    def test_all_good(self):
        """Test all good."""
        with patch(
            'app.enquiries.celery.app.control.inspect.stats',
            return_value=[{"dummy": True}]
        ):
            url = reverse('ping')
            response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert '<status>OK</status>' in str(response.content)
        assert response.headers['content-type'] == 'text/xml'

    def test_check_database_fail(self):
        url = reverse('ping')

        with patch(
            'app.enquiries.models.Enquiry.objects.exists',
            side_effect=DatabaseError('No database'),
        ):
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert '<status>FALSE</status>' in str(response.content)
            assert response.headers['content-type'] == 'text/xml'

    def test_check_celery_fail(self):
        url = reverse('ping')
        with patch(
            'app.enquiries.celery.app.control.inspect.stats',
            return_value=None
        ):
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert '<status>FALSE</status>' in str(response.content)
            assert response.headers['content-type'] == 'text/xml'

    def test_check_redis_fail(self):
        url = reverse('ping')
        with patch(
            'redis.Redis.ping',
            side_effect=RedisError("Redis error"),
        ):
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert '<status>FALSE</status>' in str(response.content)
            assert response.headers['content-type'] == 'text/xml'
