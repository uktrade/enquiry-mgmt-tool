import csv
import pytest
import pytz
import random

from io import StringIO
from datetime import date
from faker import Faker

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse

from rest_framework import status
from unittest import mock

import app.enquiries.ref_data as ref_data
from app.enquiries import utils
from app.enquiries.models import Enquiry, Enquirer
from app.enquiries.tests.factories import (
    EnquiryFactory,
    create_fake_enquiry_csv_row,
    get_random_item,
    get_display_name,
)
from app.enquiries.views import ImportEnquiriesView

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


ERROR_MISSING_FIELD = "field cannot be blank"


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
        num_enquiries = 3
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
                [enq["id"] for enq in response.data["results"]], ids[start:end]
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
        enquiry_stage_display_name = get_display_name(
            ref_data.EnquiryStage, enquiry.enquiry_stage
        )
        country_display_name = get_display_name(ref_data.Country, enquiry.country)
        self.assertContains(response, enquiry_stage_display_name)
        self.assertContains(response, country_display_name)

    def test_enquiry_import_view(self):
        """Test retrieving a valid enquiry returns 200"""
        response = self.client.get(reverse("import-enquiries"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_enquiry_import_post_success(self):
        """
        Test a successful import
        Creates a list of enquiry dicts and ensures
        that records are written to the DB after submitting the form (POST)
        """
        num_items = 5
        enquiries = [create_fake_enquiry_csv_row() for i in range(num_items)]
        fp = StringIO()

        writer = csv.DictWriter(
            fp, fieldnames=ref_data.IMPORT_COL_NAMES, quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()
        writer.writerows(enquiries)

        body = fp.getvalue().encode()
        upload = SimpleUploadedFile("test.csv", body, content_type="text/csv")

        response = self.client.post(
            reverse("import-enquiries"), {"enquiries": upload}, follow=True
        )

        db_enquiries = Enquiry.objects.all()
        final_count = db_enquiries.count()
        self.assertNotContains(response, ImportEnquiriesView.ERROR_HEADER)
        self.assertContains(response, f"Successfully posted {num_items} records!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(final_count, num_items)

        for e in enquiries:
            # generate filter keyword args dynamically
            # (can't modify the dict we arfe iterating over withouit raising an error so make a extra copy)
            qs_kwargs = utils.csv_row_to_enquiry_filter_kwargs(e)

            self.assertTrue(Enquiry.objects.filter(**qs_kwargs).exists())

    def test_enquiry_import_post_error(self):
        """
        Test a unsuccessful import
        Creates an enquiry dict, updates few fields and ensures
        the data is updated after submitting the form
        """
        num_items = 5
        initial_count = Enquiry.objects.count()
        enquiries = [create_fake_enquiry_csv_row() for i in range(num_items)]
        enquiries[3]["enquirer_job_title"] = ""

        fp = StringIO()

        writer = csv.DictWriter(
            fp, fieldnames=ref_data.IMPORT_COL_NAMES, quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()
        writer.writerows(enquiries)

        body = fp.getvalue().encode()
        upload = SimpleUploadedFile("test.csv", body, content_type="text/csv")

        response = self.client.post(
            reverse("import-enquiries"), {"enquiries": upload}, follow=True
        )

        final_count = Enquiry.objects.count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test atomic transactions
        self.assertEqual(
            final_count,
            initial_count,
            f"atomic transaction should prevent any records being created. Found: {final_count}",
        )

    def test_enquiry_import_post_success_chunks(self):
        """
        Test a successful import over the chunk limit
        Creates a list of enquiry dicts and ensures
        that records are written to the DB after submitting the form (POST)
        """
        TEST_CHUNK_SIZE = 16000
        num_items = 0
        file_size = 0
        fp = StringIO()

        writer = csv.DictWriter(
            fp, fieldnames=ref_data.IMPORT_COL_NAMES, quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()

        with self.settings(UPLOAD_CHUNK_SIZE=TEST_CHUNK_SIZE):
            while file_size <= settings.UPLOAD_CHUNK_SIZE:
                e = create_fake_enquiry_csv_row()
                content_len = writer.writerow(e)
                file_size += content_len
                num_items += 1

            body = fp.getvalue().encode()
            upload = SimpleUploadedFile("test.csv", body, content_type="text/csv")

            response = self.client.post(
                reverse("import-enquiries"), {"enquiries": upload}, follow=True
            )

            final_count = Enquiry.objects.count()
            self.assertNotContains(response, ImportEnquiriesView.ERROR_HEADER)
            self.assertContains(response, f"Successfully posted {num_items} records!")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(num_items, final_count)
            self.assertTrue(len(body) > settings.UPLOAD_CHUNK_SIZE)
