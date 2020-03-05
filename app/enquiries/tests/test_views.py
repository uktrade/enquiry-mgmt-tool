import random

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from app.enquiries.tests.factories import EnquiryFactory


class EnquiryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_enquiry_list(self):
        enquiries = [EnquiryFactory() for i in range(5)]
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = response.data["serializer"]
        self.assertEqual(len(serializer), len(enquiries))

    def test_enquiry_detail(self):
        enquiries = [EnquiryFactory() for i in range(5)]
        response = self.client.get(
            reverse("enquiry-detail", kwargs={"pk": random.choice(enquiries).id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            reverse("enquiry-detail", kwargs={"pk": 100})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
