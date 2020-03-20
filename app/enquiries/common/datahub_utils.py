import json
import logging
import os
import requests

from django.conf import settings
from mohawk import Sender
from requests.exceptions import RequestException
from rest_framework import status


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
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.DATA_HUB_ACCESS_TOKEN}",
        }

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except RequestException as e:
        logging.error(
            f"Error {e} while requesting {url}, request timeout set to {timeout} secs"
        )
        raise e

    return response


def dh_fetch_metadata():
    """
    Fetches metadata from Data Hub as we need that to call Data Hub APIs
    """

    endpoints = (
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

    credentials = settings.HAWK_CREDENTIALS[settings.HAWK_ID]

    metadata = {"failed": []}
    for endpoint in endpoints:
        meta_url = os.path.join(settings.DATA_HUB_METADATA_URL, endpoint)

        print(f"Fetching {meta_url} ...")

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
        print(f"Failed to fetch Data Hub metadata for endpoints: {metadata['failed']}")

    return metadata


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
    # Access token is invalid, consider that there are no matches
    if response.status_code != status.HTTP_200_OK:
        return companies

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

    return companies


def dh_contact_search(contact_name):
    """
    Peforms a Contact name search using Data hub API.

    Returns list of subset of fields for each contact found
    """
    url = settings.DATA_HUB_CONTACT_SEARCH_URL
    payload = {"name": contact_name}

    response = dh_request("POST", url, payload)

    contacts = []
    if response.status_code != status.HTTP_200_OK:
        return contacts

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

    return contacts
