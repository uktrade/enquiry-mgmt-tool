from unittest import mock
from django.db.utils import OperationalError
from django.urls import reverse
from rest_framework import status

import app.enquiries.tests.utils as test_utils


class ServiceHealthCheckTestCase(test_utils.BaseEnquiryTestCase):
    def setUp(self):
        super().setUp()

    def test_service_status_healthy(self):
        """
        Ping service health check route and ensure we can connect
        to database and run a query
        """
        response = self.client.post(reverse("ping"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers["content-type"], ("Content-Type", "text/plain"))
        self.assertEqual(response.content.decode("utf-8"), "OK")

    @mock.patch("app.enquiries.models.Enquiry.objects")
    def test_service_status_unhealthy(self, model_manager):
        """
        Test that triggers an exception when the query is executed
        and ensures service status reported as ERROR
        """
        model_manager.exists.side_effect = OperationalError("connection failure")
        response = self.client.post(reverse("ping"))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.content.decode("utf-8"), "ERROR")
