import random

from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

import app.enquiries.ref_data as ref_data
from app.enquiries.tests.factories import EnquiryFactory, get_random_item


class EnquiryViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.client = Client()

    def get_an_enquiry_detail(self, num_enquiries=5):
        enquiries = [EnquiryFactory() for i in range(num_enquiries)]
        response = self.client.get(
            reverse("enquiry-detail", kwargs={"pk": random.choice(enquiries).id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.context["enquiry"]

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
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_enquiry_successful_update(self):
        enquiry = self.get_an_enquiry_detail()
        enquiry = model_to_dict(enquiry)
        update_fields = {
            "company_name": self.faker.company(),
            "enquiry_stage": get_random_item(ref_data.EnquiryStage),
            "notes": self.faker.sentence(),
            "country": get_random_item(ref_data.Country),
        }

        response = self.client.post(
            reverse("enquiry-edit", kwargs={"pk": enquiry["id"]}), **update_fields,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_enquiry = model_to_dict(response.context["enquiry"])
        for key in update_fields:
            self.assertEqual(enquiry[key], updated_enquiry[key])

    def test_enquiry_failed_update(self):
        enquiry = self.get_an_enquiry_detail()
        enquiry = model_to_dict(enquiry)
        update_fields = {"company_name": ""}

        response = self.client.post(
            reverse("enquiry-edit", kwargs={"pk": enquiry["id"]}), **update_fields,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_enquiry = model_to_dict(response.context["enquiry"])
        self.assertEqual(updated_enquiry["company_name"], enquiry["company_name"])
        self.assertNotEqual(updated_enquiry["company_name"], "")
