import app.enquiries.ref_data as ref_data

from django.test import TestCase
from django.test.client import RequestFactory
from faker import Faker
from unittest import mock

from app.enquiries.models import Enquirer
from app.enquiries.common.datahub_utils import (
    dh_get_matching_company_contact,
    dh_prepare_contact,
)

faker = Faker()

MATCHING_CONTACT_DETAILS = {
    "first_name": "Datahub",
    "last_name": "User",
    "email": "user@example.com",
    "id": "376fe77b",
}


def contact_search_response():
    return {
        "success": {
            "results": [
                {
                    "id": MATCHING_CONTACT_DETAILS["id"],
                    "first_name": MATCHING_CONTACT_DETAILS["first_name"],
                    "last_name": MATCHING_CONTACT_DETAILS["last_name"],
                    "job_title": "CEO",
                    "telephone_number": "123456789",
                    "email": MATCHING_CONTACT_DETAILS["email"],
                }
            ]
        },
        "error": {"detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"},
    }


class DataHubUtilsTests(TestCase):
    def setUp(self):
        self.matching_enquirer = Enquirer.objects.create(
            first_name=MATCHING_CONTACT_DETAILS["first_name"],
            last_name=MATCHING_CONTACT_DETAILS["last_name"],
            email=MATCHING_CONTACT_DETAILS["email"],
            job_title='Manager',
            phone_country_code='1',
            phone=faker.phone_number(),
            email_consent=True,
            phone_consent=True,
            request_for_call=ref_data.RequestForCall.YES_AFTERNOON.value,
        )
        self.partially_matching_enquirer = Enquirer.objects.create(
            first_name=MATCHING_CONTACT_DETAILS["first_name"],
            last_name=MATCHING_CONTACT_DETAILS["last_name"],
            email=faker.email(),
            job_title='Manager',
            phone_country_code='1',
            phone=faker.phone_number(),
            email_consent=True,
            phone_consent=True,
            request_for_call=ref_data.RequestForCall.YES_AFTERNOON.value,
        )
        self.new_enquirer = Enquirer.objects.create(
            first_name=faker.name(),
            last_name=faker.name(),
            email=faker.email(),
            job_title='Manager',
            phone_country_code='1',
            phone=faker.phone_number(),
            email_consent=True,
            phone_consent=True,
            request_for_call=ref_data.RequestForCall.YES_AFTERNOON.value,
        )
        self.company_results = [
            {
                "datahub_id": contact["id"],
                "first_name": contact["first_name"],
                "last_name": contact["last_name"],
                "job_title": contact["job_title"],
                "email": contact["email"],
                "phone": contact["telephone_number"],
            } for contact in contact_search_response()["success"]["results"]
        ]
        self.access_token = "mock_token"
        self.dh_company_id = "1234-5678"
        self.dh_contact_id = "1234"
        self.request = RequestFactory()
        self.error_message = "ERROR"

    def test_dh_get_matching_company_contact_match(self):
        """Test company contact match function returns matching contact"""

        contact = dh_get_matching_company_contact(
            self.matching_enquirer.first_name,
            self.matching_enquirer.last_name,
            self.matching_enquirer.email,
            self.company_results
        )
        self.assertEqual(contact["first_name"], MATCHING_CONTACT_DETAILS["first_name"])
        self.assertEqual(contact["last_name"], MATCHING_CONTACT_DETAILS["last_name"])
        self.assertEqual(contact["email"], MATCHING_CONTACT_DETAILS["email"])

    def test_dh_get_matching_company_contact_partial_match(self):
        """Test company contact match function does not return a partial match"""

        contact = dh_get_matching_company_contact(
            self.partially_matching_enquirer.first_name,
            self.partially_matching_enquirer.last_name,
            self.partially_matching_enquirer.email,
            self.company_results
        )
        self.assertIsNone(contact)

    def test_dh_get_matching_company_contact_no_match(self):
        """Test company contact match function returns None if no match"""

        contact = dh_get_matching_company_contact(
            self.new_enquirer.first_name,
            self.new_enquirer.last_name,
            self.new_enquirer.email,
            self.company_results
        )
        self.assertIsNone(contact)

    @mock.patch('app.enquiries.common.datahub_utils.dh_contact_create')
    @mock.patch('app.enquiries.common.datahub_utils.dh_get_matching_company_contact')
    @mock.patch('app.enquiries.common.datahub_utils.dh_get_company_contact_list')
    def test_dh_prepare_contact_matching_contact(
        self,
        mock_dh_contact_list, mock_matching_contact,
        mock_create_dh_contact,
    ):
        """Test contact prepare function in case of a contact match"""
        mock_dh_contact_list.return_value = [self.company_results, None]
        mock_matching_contact.return_value = {"datahub_id": self.dh_contact_id}

        contact_id, error = dh_prepare_contact(
            self.request,
            self.access_token,
            self.matching_enquirer,
            self.dh_company_id
        )

        mock_dh_contact_list.assert_called_once_with(
            self.request,
            self.access_token,
            self.dh_company_id,
        )

        mock_matching_contact.assert_called_once_with(
            self.matching_enquirer.first_name,
            self.matching_enquirer.last_name,
            self.matching_enquirer.email,
            self.company_results
        )

        mock_create_dh_contact.assert_not_called()

        self.assertEqual(contact_id, self.dh_contact_id)
        self.assertIsNone(error)

    @mock.patch('app.enquiries.common.datahub_utils.dh_contact_create')
    @mock.patch('app.enquiries.common.datahub_utils.dh_get_matching_company_contact')
    @mock.patch('app.enquiries.common.datahub_utils.dh_get_company_contact_list')
    def test_dh_prepare_contact_new_contact_existing_contacts(
        self,
        mock_dh_contact_list, mock_matching_contact,
        mock_create_dh_contact,
    ):
        """Test contact prepare function in case of company having different existing contacts"""
        mock_dh_contact_list.return_value = [self.company_results, None]
        mock_matching_contact.return_value = None
        mock_create_dh_contact.return_value = [{"id": self.dh_contact_id}, None]

        contact_id, error = dh_prepare_contact(
            self.request,
            self.access_token,
            self.new_enquirer,
            self.dh_company_id
        )

        mock_create_dh_contact.assert_called_once_with(
            self.request,
            self.access_token,
            self.new_enquirer,
            self.dh_company_id,
            primary=False)

        self.assertEqual(contact_id, self.dh_contact_id)
        self.assertIsNone(error)

    @mock.patch('app.enquiries.common.datahub_utils.dh_contact_create')
    @mock.patch('app.enquiries.common.datahub_utils.dh_get_matching_company_contact')
    @mock.patch('app.enquiries.common.datahub_utils.dh_get_company_contact_list')
    def test_dh_prepare_contact_new_contact_no_existing_contacts(
        self,
        mock_dh_contact_list, mock_matching_contact,
        mock_create_dh_contact,
    ):
        """Test contact prepare function in case of there being no existing company contacts"""
        mock_dh_contact_list.return_value = [None, None]
        mock_create_dh_contact.return_value = [{"id": self.dh_contact_id}, None]

        contact_id, error = dh_prepare_contact(
            self.request,
            self.access_token,
            self.new_enquirer,
            self.dh_company_id
        )

        mock_matching_contact.assert_not_called()

        mock_create_dh_contact.assert_called_once_with(
            self.request,
            self.access_token,
            self.new_enquirer,
            self.dh_company_id,
            primary=True)

        self.assertEqual(contact_id, self.dh_contact_id)
        self.assertIsNone(error)

    @mock.patch('app.enquiries.common.datahub_utils.dh_get_company_contact_list')
    def test_dh_prepare_contact_errors(self, mock_dh_contact_list):
        """Test contact prepare function in case of errors"""
        mock_dh_contact_list.return_value = [None, self.error_message]

        contact_id, error = dh_prepare_contact(
            self.request,
            self.access_token,
            self.new_enquirer,
            self.dh_company_id
        )

        self.assertIsNone(contact_id)
        self.assertEqual(
            error,
            {"contact_search": f"Error while checking company contacts, {self.error_message}"}
        )
