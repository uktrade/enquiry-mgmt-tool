import pytest
import pytz
import random
import requests
from bs4 import BeautifulSoup
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
from app.enquiries.tests import utils as test_utils
from app.enquiries.tests.factories import (
    EnquiryFactory,
    get_random_item,
    get_display_name,
)

faker = Faker(["en_GB", "en_US", "ja_JP"])
headers = {"HTTP_CONTENT_TYPE": "text/html", "HTTP_ACCEPT": "text/html"}


class EnquiryViewFiltersTestCase(test_utils.BaseEnquiryTestCase):
    def setUp(self):
        super().setUp()
        # self.faker = Faker()
        # self.client = Client()

    def test_enquiry_filters_render(self):
        """Test that the search filters render correctly"""
        # DRF defaults to JSON response so we need to set headers to receive HTML

        response = self.client.get(reverse("enquiry-list"), **headers)
        soup = BeautifulSoup(response.content, "html.parser")

        self.assertIsNotNone(
            soup.find(attrs={"data-qa": "search-filters"}),
            msg="should render search filters",
        )

        # users checkbox
        _input = soup.select("#owner__id")[0]
        _label = soup.select("label[for=owner__id]")[0]

        self.assertIsNotNone(
            _input, msg="should render unassigned control",
        )

        self.assertIsNotNone(
            _label, msg="should render unassigned control label",
        )

        self.assertEqual(_input.attrs.get("value"), "UNASSIGNED")
        self.assertEqual(_label.string.strip(), "Unassigned")

        # enquiry_stage checxboxes
        for value, label in ref_data.EnquiryStage.choices:
            _id = f"enquiry_stage_{value}"
            _input = soup.select(f"#{_id}")[0]
            _label = soup.select(f'label[for="{_id}"]')[0]

            self.assertIsNotNone(
                _input, msg=f"should render enquiry_stage input {label}",
            )

            self.assertIsNotNone(
                _label, msg=f"should render enquiry_stage label {label}",
            )
            self.assertEqual(_input.attrs.get("value"), value)
            self.assertEqual(_label.string.strip(), label)

        self.assertIsNotNone(
            soup.find(id="created__lt"),
            msg="should render date created before control",
        )
        self.assertIsNotNone(
            soup.find(id="created__gt"), msg="should render date created after control",
        )
        self.assertIsNotNone(
            soup.find(id="company_name__icontains"),
            msg="should render company_name control",
        )
        self.assertIsNotNone(
            soup.find(id="date_added_to_datahub__lt"),
            msg="should render date_added_to_datahub__lt control",
        )
        self.assertIsNotNone(
            soup.find(id="date_added_to_datahub__gt"),
            msg="should render date_added_to_datahub__gt control",
        )
        self.assertIsNotNone(
            soup.find(id="enquirer_email"), msg="should render enquirer_email control",
        )
        self.assertIsNotNone(
            soup.find(id="btn_submit"), msg="should render btn_submit control"
        )
