import json
import logging
import os
import requests

from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from mohawk import Sender
from requests.exceptions import RequestException
from rest_framework import status


DATA_HUB_METADATA_ENDPOINTS = (
    "country",
    "fdi-type",
    "investment-investor-type",
    "investment-involvement",
    "investment-project-stage",
    "investment-specific-programme",
    "investment-type",
    "referral-source-activity",
    "referral-source-website",
    "sector",
)

def dh_request(method, url, payload, request_headers=None, timeout=15):
    """
    Helper function to perform Data Hub request

    All requests have same headers, instead of repeating in each function
    they are added in the function. If there are any custom headers they
    can be provided using the request_headers argument.

    Each request has a timeout (default=15sec) failing which throws an
    exception which will be captured in Sentry
    """

    if request_headers:
        headers = request_headers
    else:
        # TODO: We don't need to send the access token in the headers
        # once SSO is integrated as it comes from SSO directly
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.DATA_HUB_ACCESS_TOKEN}",
        }

    try:
        if method == "GET":
            response = requests.get(
                url, headers=headers, params=params, timeout=timeout
            )
        elif method == "POST":
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except RequestException as e:
        logging.error(
            f"Error {e} while requesting {url}, request timeout set to {timeout} secs"
        )
        raise e

    return response


def _dh_fetch_metadata():
    """
    Fetches metadata from Data Hub as we need that to call Data Hub APIs
    """
    logging.info(f"Fetching metadata at {datetime.now()}")
    credentials = {
        "id": settings.DATA_HUB_HAWK_ID,
        "key": settings.DATA_HUB_HAWK_KEY,
        "algorithm": "sha256",
    }

    metadata = {"failed": []}
    for endpoint in DATA_HUB_METADATA_ENDPOINTS:
        meta_url = os.path.join(settings.DATA_HUB_METADATA_URL, endpoint)

        logging.info(f"Fetching {meta_url} ...")

        sender = Sender(
            credentials,
            meta_url,
            "GET",
            content=None,
            content_type=None,
            always_hash_content=False,
        )
        response = requests.get(
            meta_url, headers={"Authorization": sender.request_header}, timeout=10
        )
        if response.ok:
            metadata[endpoint] = response.json()
        else:
            metadata["failed"].append(endpoint)

    if metadata["failed"]:
        logging.error(f"Error fetching Data Hub metadata for endpoints: {metadata['failed']}")

    return metadata


def dh_fetch_metadata(cache_key='metadata', expiry_secs=60*60):
    """
    Fetches and caches the metadata with an expiry time

    It check if the data is valid in cache, if it has expired then fetches again
    """

    try:
        cached_metadata = cache.get(cache_key)
        if not cached_metadata:
            logging.info("Metadata expired in cache, fetching again ...")
            cached_metadata = _dh_fetch_metadata()
            cache.set(cache_key, cached_metadata, timeout=expiry_secs)
            return cached_metadata

        logging.info(f"Metadata valid in cache (expiry_secs={expiry_secs})")
        return cached_metadata
    except Exception as e:
        logging.error(f"Error fetching metadata, {str(e)} ...")
        raise e


def map_to_datahub_id(refdata_value, dh_metadata, dh_category, target_key="name"):
    """
    Maps application reference data to Data Hub reference data and
    extracts the unique identifier

    Arguments
    ---------
    refdata_value: Human readable value of a choice field
    dh_metadata: Data Hub metadata dictionary
    dh_category: Data Hub metadata category
    target_key: key name with then metadata object

    Returns
    -------
    Data Hub uuid for the given refdata_value if available otherwise None

    """

    dh_data = list(
        filter(lambda d: d[target_key] == refdata_value, dh_metadata[dh_category])
    )

    return dh_data[0]["id"] if dh_data else None


def dh_company_search(company_name):
    """
    Peforms a Company name search using Data hub API.

    Returns list of subset of fields for each company found
    """
    companies = []
    url = settings.DATA_HUB_COMPANY_SEARCH_URL
    payload = {"name": company_name}

    response = dh_request("POST", url, payload)

    # It is not an error for us if the request fails, this can happen if the
    # Access token is invalid, consider that there are no matches however
    # user is notified of the error to take appropriate action
    # TODO: revisit once SSO integration is completed
    if not response.ok:
        return companies, response.json()

    for company in response.json()["results"]:
        address = company["address"]
        companies.append(
            {
                "datahub_id": company["id"],
                "name": company["name"],
                "address": {
                    "line_1": address["line_1"],
                    "line_2": address["line_2"],
                    "town": address["town"],
                    "county": address["county"],
                    "postcode": address["postcode"],
                    "country": address["country"]["name"],
                },
            }
        )

    return companies, None


def dh_contact_search(contact_name):
    """
    Peforms a Contact name search using Data hub API.

    Returns list of subset of fields for each contact found
    """
    contacts = []
    url = settings.DATA_HUB_CONTACT_SEARCH_URL
    payload = {"name": contact_name}

    response = dh_request("POST", url, payload)

    if not response.ok:
        return contacts, response.json()

    for contact in response.json()["results"]:
        contacts.append(
            {
                "datahub_id": contact["id"],
                "first_name": contact["first_name"],
                "last_name": contact["last_name"],
                "job_title": contact["job_title"],
                "email": contact["email"],
                "phone": contact["telephone_number"],
            }
        )

    return contacts, None
