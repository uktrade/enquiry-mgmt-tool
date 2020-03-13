from unittest import mock
from django.db.utils import OperationalError
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from app.enquiries.tests.factories import EnquiryFactory


class ServiceHealthCheckTestCase(TestCase):

    def _test_service_status(self, comment):
        """ Ping service health check route and ensure all is good """
        response = self.client.post(reverse("ping"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'text/xml'))
        self.assertEqual('<status>OK</status>' in str(response.content), True)
        self.assertEqual(f'{comment}' in str(response.content), True)

    def test_service_status_healthy_no_enquiries(self):
        """
        Test that database connection is successful and can run a query
        It is possible that no enquiries exists in database when launched,
        it cannot be considered as service failure
        """
        self._test_service_status("No Enquiries exists")

    def test_service_status_healthy_with_enquiries(self):
        """
        Test that database connection is successful and can run a query
        when there are atleast 1 enquiry in the database
        """
        enquiries = EnquiryFactory.create_batch(2)
        self._test_service_status("Atleast one Enquiry exists")

    @mock.patch("app.enquiries.models.Enquiry.objects")
    def test_service_status_unhealthy(self, mgr):
        """
        Test that triggers an exception when the query is executed
        and ensures service status reported as ERROR
        """
        mgr.all.side_effect = OperationalError("connection failure")
        response = self.client.post(reverse("ping"))
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual('<status>ERROR</status>' in str(response.content), True)
