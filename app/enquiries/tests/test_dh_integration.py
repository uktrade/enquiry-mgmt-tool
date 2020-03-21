import pytest
import requests

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from requests.exceptions import Timeout
from rest_framework import status
from unittest import mock

from app.enquiries.common.datahub_utils import dh_request, dh_fetch_metadata


class DataHubIntegrationTests(TestCase):
    @mock.patch("requests.post")
    def test_dh_request_timeout(self, mock_post):
        """ Tests to ensure data hub requests raise exception """
        mock_post.side_effect = Timeout
        url = settings.DATA_HUB_COMPANY_SEARCH_URL
        payload = {"name": "test"}

        with pytest.raises(Timeout):
            response = dh_request("POST", url, payload, timeout=2)

    @mock.patch("django.core.cache.cache.get")
    def test_dh_fetch_metada_exception(self, mock_cache_get):
        """ Ensure any exception during metadata fetch handled gracefully """
        mock_cache_get.side_effect = Exception

        with pytest.raises(Exception):
            metadata = dh_fetch_metadata()
            self.assertEqual(metadata, None)
