import csv
import pytest
import pytz
import random
from openpyxl import Workbook, load_workbook

from io import StringIO
from datetime import date, datetime
from faker import Faker

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.models import model_to_dict
from django.urls import reverse

from rest_framework import status
from unittest import mock

import app.enquiries.ref_data as ref_data
import app.enquiries.views as enquiry_views
import app.enquiries.tests.utils as test_utils
from app.enquiries import utils
from app.enquiries.models import Enquiry, Enquirer
from app.enquiries.tests.factories import (
    EnquirerFactory,
    EnquiryFactory,
    create_fake_enquiry_csv_row,
    get_random_item,
    get_display_name,
    get_display_value,
    return_display_value,
)
from app.enquiries.views import ImportEnquiriesView

faker = Faker(["en_GB", "en_US", "ja_JP"])
headers = {"HTTP_CONTENT_TYPE": "text/html", "HTTP_ACCEPT": "text/html"}
headers_json = {"HTTP_CONTENT_TYPE": "text/html", "HTTP_ACCEPT": "application/json"}

enquiry_field_names = [f.name for f in Enquiry._meta.fields]
enquirer_field_names = [f.name for f in Enquirer._meta.fields]


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
            "phone_country_code": random.randint(1, 100),
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


class EnquiryViewTestCase(test_utils.BaseEnquiryTestCase):
    def setUp(self):
        super().setUp()

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
    
    def assert_factory_enquiry_equals_enquiry_response(self, factory_item, response_item):
        date_fields = [
            "created",
            "modified",
            "date_added_to_datahub",
            "project_success_date",
        ]
        omit_fields = ["owner"]
        ref_fields = ref_data.MAP_ENQUIRY_FIELD_TO_REF_DATA

        for name in enquiry_field_names:
            if name == "enquirer":
                continue
            factory_value = getattr(factory_item, name)
            db_value = response_item[name]
            if name in omit_fields:
                continue
            elif name in date_fields:
                if isinstance(db_value, datetime):
                    db_value = db_value.date()
                elif isinstance(db_value, str):
                    db_value = datetime.strptime(db_value, "%d %B %Y")
                    db_value = (
                        db_value.date()
                        if isinstance(db_value, datetime)
                        else db_value
                    )
                factory_value = (
                    factory_value.date() if isinstance(factory_value, datetime) else factory_value
                )
            elif name in ref_fields:
                ref_model = ref_fields[name]
                db_value = return_display_value(ref_model, db_value)
                pass

            self.assertEqual(factory_value, db_value)

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
            response = self.client.get(
                reverse("enquiry-list"), {"page": page + 1}, **headers
            )
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
        data["phone_country_code"] = enquirer.phone_country_code
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
    
    def test_helper_login(self):
        result = self.login()
        self.assertEqual(result, True)
        self.assertEqual(self.logged_in, True)
        self.assertEqual(result, self.logged_in)

    def test_login_protected(self):
        """Test the view is protected by SSO"""
        self.logout()
        response = self.client.get(reverse("enquiry-list"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.get("Location").split("?")[0], settings.LOGIN_URL)
        self.login()

    def test_enquiry_list_filtered(self):
        """Test retrieving enquiry list and ensure we get expected count"""
        EnquiryFactory(company_name="Foo Bar")
        EnquiryFactory(company_name="Bar Inc")
        EnquiryFactory(company_name="Baz")
        response = self.client.get(
            reverse("enquiry-list"), {"company_name__icontains": "Bar"}, **headers
        )
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 2)

    def test_enquiry_list_filtered_unassigned(self):
        """Test retrieving enquiry list and ensure we get expected count"""
        

        EnquirerFactory()
        enquiries = [
            EnquiryFactory(enquiry_stage=ref_data.EnquiryStage.ADDED_TO_DATAHUB),
            EnquiryFactory(enquiry_stage=ref_data.EnquiryStage.AWAITING_RESPONSE),
            EnquiryFactory(enquiry_stage=ref_data.EnquiryStage.NEW),
        ]

        owner = enquiries[1].owner
        enquiries[0].owner = None
        enquiries[0].save()
        enquiry_unassigned = enquiries[0]
        enquiry_assigned = enquiries[1]

        # owner assigned
        response = self.client.get(
            reverse("enquiry-list"), {"owner__id": owner.id}, **headers
        )
        data = response.data
        
        enquiry_data = data["results"][0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assert_factory_enquiry_equals_enquiry_response(enquiry_assigned, enquiry_data)
        

        # owner unassigned
        response = self.client.get(reverse("enquiry-list"), {"owner__id": "UNASSIGNED"})
        data = response.data

        enquiry_data_unassigned = data["results"][0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)

        self.assert_factory_enquiry_equals_enquiry_response(enquiry_unassigned, enquiry_data_unassigned)

    def test_enquiry_list_filtered_enquiry_stage(self):
        """Test retrieving enquiry list and ensure we get expected count"""
        EnquiryFactory(enquiry_stage=ref_data.EnquiryStage.ADDED_TO_DATAHUB),
        EnquiryFactory(enquiry_stage=ref_data.EnquiryStage.AWAITING_RESPONSE),
        EnquiryFactory(enquiry_stage=ref_data.EnquiryStage.NEW)
        # enquiry stage - ADDED_TO_DATAHUB
        response = self.client.get(
            reverse("enquiry-list"),
            {"enquiry_stage": ref_data.EnquiryStage.ADDED_TO_DATAHUB},
        )
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)

        # enquiry stage - NON_FDI
        response = self.client.get(
            reverse("enquiry-list"), {"enquiry_stage": ref_data.EnquiryStage.NON_FDI}
        )
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 0)

    def test_import_template(self):
        """Tests that the dynamically generated .XLSX template is accessible has the correct format.
        The spreadsheet has multiple sheets with the 'enquiries' sheet used to capture user input.
        All other sheets are populate with the apps ref_data.py
        """
        import io
        import tempfile

        response = self.client.get(reverse("import-template"))
        content = response.content

        wb = load_workbook(io.BytesIO(content))
        sheet = wb.active
        for row in sheet.values:
            for i, val in enumerate(row):
                self.assertEqual(
                    val,
                    ref_data.IMPORT_COL_NAMES[i],
                    msg="should match expected column value",
                )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            enquiry_views.ImportTemplateDownloadView.CONTENT_TYPE,
            response.get("Content-Type"),
            msg=f"Should have content type: {enquiry_views.ImportTemplateDownloadView.CONTENT_TYPE}",
        )
        self.assertIn(
            settings.IMPORT_TEMPLATE_FILENAME, response.get("Content-Disposition")
        )
