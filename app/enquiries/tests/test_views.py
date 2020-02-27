import pytz
import random
from datetime import date
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

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


class EnquiryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def create_enquiry(self, enquiry):
        response = self.client.post(
            reverse("enquiry-list"), data=enquiry, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()

    def test_enquiry_list(self):
        enquiries = [self.create_enquiry(canned_enquiry()) for i in range(5)]
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = response.data["serializer"]
        self.assertEqual(len(serializer), len(enquiries))

    def test_enquiry_create(self):
        enquiry = canned_enquiry()
        response = self.create_enquiry(enquiry)
        self.assertEqual(response["company_name"], enquiry["company_name"])

    def test_enquiry_create_missing_mandatory_field(self):
        enquiry = canned_enquiry()
        del enquiry["company_name"]
        response = self.client.post(
            reverse("enquiry-list"), data=enquiry, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_email_already_exists_error(self):
        enquiry = canned_enquiry()
        response = self.create_enquiry(enquiry)
        self.assertEqual(response["company_name"], enquiry["company_name"])

        response = self.client.post(
            reverse("enquiry-list"), data=enquiry, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["enquirer"]["email"][0],
            "enquirer with this email already exists.",
        )
