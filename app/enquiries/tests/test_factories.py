from django.test import TestCase

import app.enquiries.ref_data as ref_data
from app.enquiries import serializers
from app.enquiries.tests.factories import (
    EnquiryFactory,
    EnquirerFactory,
    return_display_value,
)


class EnquiriesFactoriesTestCase(TestCase):
    def test_get_display_name(self):
        option = {
            "label": "Awaiting response from Investor",
            "value": "AWAITING_RESPONSE"
        }
        expected = return_display_value(ref_data.EnquiryStage, option["label"])
        self.assertEqual(expected, option["value"])