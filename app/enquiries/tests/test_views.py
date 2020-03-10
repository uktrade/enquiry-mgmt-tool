import random

from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

import app.enquiries.ref_data as ref_data
from app.enquiries.tests.factories import EnquiryFactory, get_random_item, get_display_name


class EnquiryViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.client = Client()

    def get_an_enquiry_detail(self):
        """Helper function to get a single enquiry and retrieve details"""
        enquiry = EnquiryFactory()
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": enquiry.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.context["enquiry"]

    def test_enquiry_list(self):
        """Test retrieving enquiry list and ensure we get expected count"""
        enquiries = [EnquiryFactory() for i in range(5)]
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = response.data["serializer"]
        self.assertEqual(len(serializer), len(enquiries))

    def test_enquiry_detail(self):
        """Test retrieving a valid enquiry returns 200"""
        enquiry = EnquiryFactory()
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": enquiry.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_enquiry_detail_nonexistent_id(self):
        """Test retrieving non-existent enquiry returns 404"""
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_enquiry_successful_update(self):
        """
        Test a successful update
        Creates an enquiry first, updates few fields and ensures
        the data is updated after submitting the form
        """
        enquiry = model_to_dict(EnquiryFactory())
        # TODO: remove blank fields
        # POST request to a form expects all the fields but sending optional
        # fields whose value is None causing form_invalid errors.
        # Setting content-type as json also not helping, ignore blank fields
        data = {k: v for k, v in enquiry.items() if v}
        data["company_name"] = self.faker.company()
        data["enquiry_stage"] = get_random_item(ref_data.EnquiryStage)
        data["notes"] = self.faker.sentence()
        data["country"] = get_random_item(ref_data.Country)
        response = self.client.post(
            reverse("enquiry-edit", kwargs={"pk": data["id"]}), data,
        )
        # POST request response to a form is 302
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # retrieve updated record
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": data["id"]}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated = model_to_dict(response.context["enquiry"])
        self.assertEqual(updated["company_name"], data["company_name"])
        self.assertEqual(updated["enquiry_stage"], data["enquiry_stage"])
        self.assertEqual(updated["notes"], data["notes"])
        self.assertEqual(updated["country"], data["country"])

    def test_enquiry_failed_update(self):
        """
        Test an unsuccessful update
        Creates an enquiry first, submits invalid data to a mandatory field
        and ensures the data is not updated after submitting the form
        """
        enquiry = self.get_an_enquiry_detail()
        enquiry = model_to_dict(enquiry)

        response = self.client.post(
            reverse("enquiry-edit", kwargs={"pk": enquiry["id"]}), {"company_name": ""},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        updated_enquiry = model_to_dict(response.context["enquiry"])
        self.assertEqual(updated_enquiry["company_name"], enquiry["company_name"])
        self.assertNotEqual(updated_enquiry["company_name"], "")

    def test_enquiry_detail_template_simple(self):
        """Test the template is using the right variables to show enquiry data 
        in the simple case when data is a string"""
        enquiry = EnquiryFactory()
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": enquiry.id}))
        self.assertContains(response, enquiry.company_name)
        self.assertContains(response, enquiry.notes)
    
    def test_enquiry_detail_template_ref_data(self):
        """Test the template is using the right variables to show enquiry data 
        in the case when data is a ref_data choice and has a verbose name"""
        enquiry = EnquiryFactory()
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": enquiry.id}))
        enquiry_stage_display_name = get_display_name(ref_data.EnquiryStage, enquiry.enquiry_stage)
        country_display_name = get_display_name(ref_data.Country, enquiry.country)
        self.assertContains(response, enquiry_stage_display_name)
        self.assertContains(response, country_display_name)
