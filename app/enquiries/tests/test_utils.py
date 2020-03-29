
from django.test import Client, TestCase
from faker import Faker

import app.enquiries.tests.utils as test_utils
from app.enquiries import models, ref_data, utils

from app.enquiries.tests.factories import (
    create_fake_enquiry_csv_row,
    get_random_item,
    get_display_name,
)

class EnquiryViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.client = Client()

    def test_csv_row_to_enquiry_filter(self):
        """
        Tests that the util function returns the expected dict keys and values
        """
        csv_data = create_fake_enquiry_csv_row()
        expected_kwargs = {
            key.replace('enquirer_', 'enquirer__'): value
            for key, value in csv_data.items()
        }

        qs_kwargs = utils.csv_row_to_enquiry_filter_kwargs(csv_data)

        self.assertEqual(
            len(expected_kwargs.keys()),
            len(qs_kwargs.keys())
            )
        
        for key in expected_kwargs:
            self.assertTrue(key in qs_kwargs)
            self.assertEqual(qs_kwargs[key], expected_kwargs[key])

    def test_util_row_to_enquiry(self):
        """
        Tests that the utility functions create the enquiry record with the correct data
        """
        csv_data = create_fake_enquiry_csv_row()
        utils.row_to_enquiry(csv_data)
        qs_args = utils.csv_row_to_enquiry_filter_kwargs(csv_data)

        exists = models.Enquiry.objects.filter(
            **qs_args
        ).exists()
        self.assertTrue(exists)


class UtilsTestCase(test_utils.BaseEnquiryTestCase):
    def test_helper_logout(self):
        """
        Tests that the `self.logged` property is correctly set when logging in/out
        """
        self.login()
        self.assertEqual(self.logged_in, True)
        self.logout()
        self.assertEqual(self.logged_in, False)
        # re-authenticate so subsequent tests can pass
        self.login()
