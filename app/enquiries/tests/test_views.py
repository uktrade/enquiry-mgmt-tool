<<<<<<< HEAD
import random

from django.forms.models import model_to_dict
=======
import pytz
import random
from datetime import datetime
>>>>>>> Update api to add new Enquiries
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

<<<<<<< HEAD
import app.enquiries.ref_data as ref_data
from app.enquiries.tests.factories import EnquiryFactory, get_random_item
=======
from app.enquiries.tests.factories import EnquiryFactory, get_random_item
import app.enquiries.ref_data as ref_data


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
        # "enquirer_first_name": faker.first_name(),
        # "enquirer_last_name": faker.last_name(),
        # "job_title": "Director",
        # "enquirer_email": faker.email(),
        # "enquirer_phone": faker.phone_number(),
        # "email_consent": random.choice([True, False]),
        # "phone_consent": random.choice([True, False]),
        # "request_for_call": get_random_item(ref_data.RequestForCall),
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
        "specific_investment_programme": ref_data.InvestmentProgram.IIGB,
        "crm": "Data Hub user 1",
        "project_code": "42901",
        "date_added_to_datahub": datetime(2020, 2, 3, 10, 20, 30, tzinfo=pytz.UTC),
        "datahub_project_status": get_random_item(ref_data.DatahubProjectStatus),
        "project_success_date": datetime(2022, 2, 3, 16, 25, 40, tzinfo=pytz.UTC),
    }
>>>>>>> Update api to add new Enquiries


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
