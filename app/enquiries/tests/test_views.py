import pytest
import pytz
import random

from datetime import date
from django.conf import settings
from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from unittest import mock

import app.enquiries.ref_data as ref_data
from app.enquiries.models import Enquiry, Enquirer
from app.enquiries.tests.factories import (
    EnquiryFactory,
    get_random_item,
    get_display_name,
)

faker = Faker(["en_GB", "en_US", "ja_JP"])


def canned_enquiry():
    return {
        "company_name": faker.company(),
        "enquiry_stage": get_random_item(ref_data.EnquiryStage),
        "enquiry_text": faker.text(),
        "investment_readiness": get_random_item(ref_data.InvestmentReadiness),
        "quality": ref_data.Quality.DEFAULT,
        "marketing_channel": get_random_item(ref_data.MarketingChannel),
        "how_they_heard_dit": get_random_item(ref_data.HowDidTheyHear),
        "website": "https://www.example.com/",
        "primary_sector": get_random_item(ref_data.PrimarySector),
        "ist_sector": get_random_item(ref_data.IstSector),
        "company_hq_address": faker.address(),
        "country": get_random_item(ref_data.Country),
        "region": get_random_item(ref_data.Region),
        "enquirer": {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "job_title": "Director",
            "email": faker.email(),
            "phone": faker.phone_number(),
            "email_consent": random.choice([True, False, False, False, True]),
            "phone_consent": random.choice([True, False, True, True, False]),
            "request_for_call": get_random_item(ref_data.RequestForCall),
        },
        "first_response_channel": get_random_item(ref_data.FirstResponseChannel),
        "notes": faker.text(),
        "first_hpo_selection": ref_data.HpoSelection.DEFAULT,
        "second_hpo_selection": ref_data.HpoSelection.DEFAULT,
        "third_hpo_selection": ref_data.HpoSelection.DEFAULT,
        "organisation_type": get_random_item(ref_data.OrganisationType),
        "investment_type": get_random_item(ref_data.InvestmentType),
        "project_name": faker.name(),
        "project_description": faker.text(),
        "anonymised_project_description": faker.text(),
        "estimated_land_date": None,
        "new_existing_investor": get_random_item(ref_data.NewExistingInvestor),
        "investor_involvement_level": ref_data.InvestorInvolvement.FDI_HUB_POST,
        "specific_investment_programme": ref_data.InvestmentProgramme.IIGB,
        "crm": "Data Hub user 1",
        "project_code": "42901",
        "date_added_to_datahub": date(2020, 2, 3),
        "datahub_project_status": get_random_item(ref_data.DatahubProjectStatus),
        "project_success_date": date(2022, 2, 3),
    }

REST_FRAMEWORK_TEST = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


class EnquiryViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.client = Client()

    def assert_dicts_equal(self, expected, actual, exclude_keys=None):
        """
        Asserts values of expected and actual dictionary objects
        Some of the keys are only available in actual (eg id), they can
        be skipped using exclude_keys
        """
        if not exclude_keys:
            exclude_keys = []

        for key, value in expected.items():
            if key in exclude_keys:
                continue

            self.assertEqual(value, expected[key])

    def create_enquiry_and_assert(self, enquiry):
        """Creates an Enquiry using the API and asserts on the response status"""
        response = self.client.post(
            reverse("enquiry-create"), data=enquiry, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()

    def get_an_enquiry_detail(self):
        """Helper function to get a single enquiry and retrieve details"""
        enquiry = EnquiryFactory()
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": enquiry.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.context["enquiry"]

    def test_enquiry_list(self):
        """Test retrieving enquiry list and ensure we get expected count"""
        enquiries = [EnquiryFactory() for i in range(2)]
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        results = response["results"]
        self.assertEqual(len(results), len(enquiries))

    def test_enquiries_list_pagination(self):
        """
        Tests pagination of enquiries list view.
        Creates enquiries and retrieves single page of results each time
        and ensures we get the expected number of results for that page.
        It will be same for all pages except for the last page
        if num_enquiries is not a multiple of page_size
        """
        num_enquiries = 13
        enquiries = EnquiryFactory.create_batch(num_enquiries)
        ids = [e.id for e in enquiries]
        page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
        total_pages = (num_enquiries + page_size - 1) // page_size
        for page in range(total_pages):
            start = page * page_size
            end = start + page_size
            response = self.client.get(reverse("enquiry-list"), {"page": page + 1})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                [enq["id"] for enq in response.data["results"]],
                ids[start:end]
            )
            self.assertEqual(response.data["current_page"], page + 1)

        # Ensure accesing the page after the last page should return 404
        response = self.client.get(reverse("enquiry-list"), {"page": total_pages + 1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_enquiry_create(self):
        """Creates an Enquiry and ensures response fields match with the request"""
        enquiry = canned_enquiry()
        response = self.create_enquiry_and_assert(enquiry)
        self.assert_dicts_equal(
            enquiry,
            response,
            ["enquirer", "date_added_to_datahub", "project_success_date"],
        )
        self.assert_dicts_equal(enquiry["enquirer"], response["enquirer"])

    def test_enquiry_create_missing_mandatory_field(self):
        """Test to ensure Enquiry creation fails if a mandatory field is not supplied"""
        enquiry = canned_enquiry()
        del enquiry["company_name"]
        response = self.client.post(
            reverse("enquiry-create"), data=enquiry, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("app.enquiries.models.Enquiry.objects")
    def test_enquiry_atomic_create(self, mock_enquiry):
        """
        While creating an Enquiry we first have to create an Enquirer instance
        as there is a foreign key reference to it. To avoid dangling Enquirers
        both of these are executed as atomic transaction. This test ensures that
        the atomic transaction is working as expected.

        We intentionally fail the Enquiry creation and assert that no new
        Enquirers are created.
        """
        num_enquirers = Enquirer.objects.all().count()
        mock_enquiry.create.side_effect = Exception(
            "raise Exception while creating Enquiry"
        )

        with pytest.raises(Exception) as e:
            enquiry = canned_enquiry()
            response = self.create_enquiry_and_assert(enquiry)
        self.assertEqual(Enquirer.objects.all().count(), num_enquirers)

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
        enquiry_obj = EnquiryFactory()
        enquiry = model_to_dict(enquiry_obj)
        # TODO: remove blank fields
        # POST request to a form expects all the fields but sending optional
        # fields whose value is None causing form_invalid errors.
        # Setting content-type as json also not helping, ignore blank fields
        data = {k: v for k, v in enquiry.items() if v}
        data["company_name"] = self.faker.company()
        data["enquiry_stage"] = get_random_item(ref_data.EnquiryStage)
        data["notes"] = self.faker.sentence()
        data["country"] = get_random_item(ref_data.Country)

        # Enquirer fields are also sent in a single form update
        enquirer = enquiry_obj.enquirer
        data["enquirer"] = enquirer.id
        data["first_name"] = "updated first name"
        data["last_name"] = enquirer.last_name
        data["job_title"] = enquirer.job_title
        data["email"] = enquirer.email
        data["phone"] = enquirer.phone
        data["email_consent"] = False
        data["phone_consent"] = True
        data["request_for_call"] = enquirer.request_for_call
        response = self.client.post(
            reverse("enquiry-edit", kwargs={"pk": data["id"]}), data,
        )
        # POST request response to a form is 302
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # retrieve updated record
        response = self.client.get(reverse("enquiry-detail", kwargs={"pk": data["id"]}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated = response.context["enquiry"]
        self.assertEqual(updated.company_name, data["company_name"])
        self.assertEqual(updated.enquiry_stage, data["enquiry_stage"])
        self.assertEqual(updated.notes, data["notes"])
        self.assertEqual(updated.country, data["country"])
        self.assertEqual(updated.enquirer.first_name, "updated first name")
        self.assertEqual(updated.enquirer.email_consent, False)
        self.assertEqual(updated.enquirer.phone_consent, True)

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
        enquiry_stage_display_name = get_display_name(
            ref_data.EnquiryStage, enquiry.enquiry_stage
        )
        country_display_name = get_display_name(ref_data.Country, enquiry.country)
        self.assertContains(response, enquiry_stage_display_name)
        self.assertContains(response, country_display_name)
