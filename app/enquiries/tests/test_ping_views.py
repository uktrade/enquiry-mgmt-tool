from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status


class ServiceHealthCheckTestCase(TestCase):

    def test_service_status_healthy(self):
        """ Ping service health check route and ensure all is good """
        response = self.client.post(reverse("ping"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['content-type'], ('Content-Type', 'text/xml'))
        self.assertEqual('<status>OK</status>' in str(response.content), True)