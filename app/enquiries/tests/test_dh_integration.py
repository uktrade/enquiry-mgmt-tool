import pytest
import requests

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from requests.exceptions import Timeout
from rest_framework import status
from unittest import mock

from app.enquiries.common.datahub_utils import dh_request


class DataHubIntegrationTests(TestCase):
    @mock.patch("requests.request")
    def test_dh_request_timeout(self, mock_request):
        """ Tests to ensure data hub requests raise exception """
        mock_request.side_effect = Timeout
        url = settings.DATA_HUB_COMPANY_SEARCH_URL
        payload = {"name": "test"}

        with pytest.raises(Timeout):
            response = dh_request("POST", url, payload, timeout=2)
