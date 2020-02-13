import pytest

from django.forms.models import model_to_dict
from django.test import TestCase

from app.enquiries.models import Enquiry
from app.enquiries.tests.factories import EnquiryFactory


# mark the whole module for db use
pytestmark = pytest.mark.django_db


class EnquiryTest(TestCase):
    """Tests for Enquiry model """

    def test_enquiry_model_creation(self):
        enquiry = EnquiryFactory()
        self.assertTrue(isinstance(enquiry, Enquiry))
        self.assertEqual(Enquiry.objects.count(), 1)
