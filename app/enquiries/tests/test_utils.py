import codecs
import csv
import io


from django.test import Client, TestCase
from faker import Faker

import app.enquiries.tests.utils as test_utils
from app.enquiries import models, ref_data, utils

from app.enquiries.tests.factories import (
    EnquiryFactory,
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

    def test_util_export_to_csv(self):
        """
        Tests that the export to csv util writes the expected data to file
        """
        enquiries = EnquiryFactory.create_batch(5)
        qs = models.Enquiry.objects.all()
        fp = io.StringIO()

        utils.export_to_csv(qs, fp)
        reader = csv.DictReader(fp)
        row_count = 0

        fp.seek(0)

        for i, enquiry_row in enumerate(reader):
            enquiry = models.Enquiry.objects.get(id=int(enquiry_row["id"]))
            for name in utils.ENQUIRY_OWN_FIELD_NAMES:
                enquiry_val = getattr(enquiry, name)
                self.assertEqual(
                    enquiry_row[name], str(enquiry_val) if enquiry_val != None else ""
                )
            if enquiry.enquirer:
                for enquirer_name in utils.ENQUIRER_FIELD_NAMES:
                    # not sure why _meta.get_fields is returning "enquirer" but skip it
                    if enquirer_name in ["enquirer"]:
                        continue
                    row_col = f"enquirer_{enquirer_name}"
                    enquirer_val = getattr(enquiry.enquirer, enquirer_name)
                    
                    self.assertEqual(
                        enquiry_row[row_col], str(enquirer_val) if enquirer_val != None else ""
                    )
            row_count += 1
        self.assertEqual(row_count, 5)
