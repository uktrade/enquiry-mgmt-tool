import pytest
import requests
import requests_mock
import time

from datetime import date
from django.conf import settings
from django.core.cache import cache
from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from requests.exceptions import Timeout
from rest_framework import status
from unittest import mock
from app.enquiries.tests.factories import EnquiryFactory

from app.enquiries.common.datahub_utils import (
    dh_request,
    dh_fetch_metadata,
    dh_company_search,
    dh_contact_search,
    dh_investment_create,
    DATA_HUB_METADATA_ENDPOINTS,
)


metadata_test_responses = {
    endpoint: {"metadata": f"metadata for {endpoint}"}
    for endpoint in DATA_HUB_METADATA_ENDPOINTS
}


def company_search_response():
    # includes subset of fields only
    return {
        "success": {
            "results": [
                {
                    "address": {
                        "line_1": "51 test street",
                        "line_2": "",
                        "country": {"name": "United Kingdom"},
                        "town": "Test town",
                        "county": "",
                        "postcode": "SN123 678",
                    },
                    "id": "80756b9a",
                    "duns_number": None,
                    "company_number": None,
                    "name": "This is a test company",
                }
            ]
        },
        "error": {"name": ["This field may not be blank."]},
    }


def contact_search_response():
    return {
        "success": {
            "results": [
                {
                    "id": "376fe77b",
                    "first_name": "Datahub",
                    "last_name": "User",
                    "job_title": "CEO",
                    "telephone_number": "123456789",
                    "email": "user@example.com",
                }
            ]
        },
        "error": {"name": ["This field may not be blank."]},
    }


class DataHubIntegrationTests(TestCase):
    @mock.patch("requests.post")
    def test_dh_request_timeout(self, mock_post):
        """ Tests to ensure data hub requests raise exception """
        mock_post.side_effect = Timeout
        url = settings.DATA_HUB_COMPANY_SEARCH_URL
        req = RequestFactory()
        post_req = req.post("/investment/", {"name": "test"})
        post_req.session = {
            settings.AUTHBROKER_TOKEN_SESSION_KEY: {"access_token": "mock_token"}
        }
        payload = {"name": "test"}

        with pytest.raises(Timeout):
            response = dh_request(
                post_req, "access_token", "POST", url, payload, timeout=2
            )

    @mock.patch("django.core.cache.cache.get")
    def test_dh_fetch_metada_exception(self, mock_cache_get):
        """ Ensure any exception during metadata fetch handled gracefully """
        mock_cache_get.side_effect = Exception

        with pytest.raises(Exception):
            metadata = dh_fetch_metadata()
            self.assertEqual(metadata, None)

    def test_dh_metadata_caching(self):
        """ Test to ensure metadata is not fetched if it is valid in cache """
        metadata = {
            "country": ["UK", "US"],
            "sector": ["Aerospace", "Advanced Engineering"],
        }
        cache.set("metadata", metadata)

        with mock.patch("app.enquiries.common.datahub_utils") as mock_dh:
            cached_metadata = dh_fetch_metadata()
            self.assertEqual(metadata, cached_metadata)
            mock_dh._dh_fetch_metadata.assert_not_called()

    def test_metadata_fetch(self):
        """ Test to ensure we fetch metadata if it is invalidated in cache """
        cache.clear()
        with requests_mock.Mocker() as m:
            for endpoint in DATA_HUB_METADATA_ENDPOINTS:
                url = f"{settings.DATA_HUB_METADATA_URL}/{endpoint}"
                m.get(url, json=metadata_test_responses[endpoint])

            self.assertIsNone(cache.get("metadata"))
            cached_metadata = dh_fetch_metadata()
            self.assertListEqual(cached_metadata.pop("failed"), [])
            self.assertEqual(cached_metadata, metadata_test_responses)
            self.assertIsNotNone(cache.get("metadata"))

    def test_company_search_success(self):
        """ Test company search returns matches """
        with requests_mock.Mocker() as m:
            url = settings.DATA_HUB_COMPANY_SEARCH_URL
            m.post(url, json=company_search_response()["success"])
            expected = company_search_response()["success"]["results"]

            response, error = dh_company_search("mock_request", "access_token", "test")
            self.assertIsNone(error)
            self.assertEqual(len(response), 1)
            self.assertEqual(response[0]["datahub_id"], expected[0]["id"])
            self.assertEqual(response[0]["name"], expected[0]["name"])

    def test_company_search_error(self):
        """ Test company search error case eg if input is blank """
        with requests_mock.Mocker() as m:
            url = settings.DATA_HUB_COMPANY_SEARCH_URL
            m.post(url, status_code=400, json=company_search_response()["error"])
            expected = company_search_response()["error"]

            response, error = dh_company_search("mock_request", "access_token", "")
            self.assertIsNotNone(error)
            self.assertEqual(error["name"], expected["name"])

    def test_contact_search_success(self):
        """ Test contact search returns matches """
        with requests_mock.Mocker() as m:
            url = settings.DATA_HUB_CONTACT_SEARCH_URL
            m.post(url, json=contact_search_response()["success"])
            expected = contact_search_response()["success"]["results"]

            response, error = dh_contact_search(
                "mock_request", "access_token", "User", "company_id"
            )
            self.assertIsNone(error)
            self.assertEqual(len(response), 1)
            self.assertEqual(response[0]["datahub_id"], expected[0]["id"])
            self.assertEqual(response[0]["first_name"], expected[0]["first_name"])
            self.assertEqual(response[0]["last_name"], expected[0]["last_name"])

    def test_contact_search_error(self):
        """ Test contact search error case eg if input is blank """
        with requests_mock.Mocker() as m:
            url = settings.DATA_HUB_CONTACT_SEARCH_URL
            m.post(url, status_code=400, json=contact_search_response()["error"])
            expected = contact_search_response()["error"]

            response, error = dh_contact_search(
                "mock_request", "access_token", "", "company_id"
            )
            self.assertIsNotNone(error)
            self.assertEqual(error["name"], expected["name"])

    def test_investment_creation_fails_company_not_in_dh(self):
        """ Test that we cannot create investment if company doesn't exist in Data Hub """
        enquiry = EnquiryFactory()
        req = RequestFactory()
        post_req = req.post("/investment/", {"name": "test"})
        post_req.session = {
            settings.AUTHBROKER_TOKEN_SESSION_KEY: {"access_token": "mock_token"}
        }
        response = dh_investment_create(post_req, enquiry)
        self.assertEqual(
            response["errors"][0]["company"],
            f"{enquiry.company_name} doesn't exist in Data Hub",
        )

    def test_investment_enquiry_cannot_submit_twice(self):
        """ If an enquiry is already submitted ensure it cannot be sent again """
        enquiry = EnquiryFactory()
        req = RequestFactory()
        post_req = req.post("/investment/", {"name": "test"})
        post_req.session = {
            settings.AUTHBROKER_TOKEN_SESSION_KEY: {"access_token": "mock_token"}
        }
        enquiry.dh_company_id = "1234-2468"
        enquiry.date_added_to_datahub = date.today()
        enquiry.save()
        response = dh_investment_create(post_req, enquiry)
        prev_date = enquiry.date_added_to_datahub.strftime("%d %B %Y")
        stage = enquiry.get_datahub_project_status_display()
        self.assertEqual(
            response["errors"][0]["enquiry"],
            f"Enquiry can only be submitted once, previously submitted on {prev_date}, stage {stage}",
        )
