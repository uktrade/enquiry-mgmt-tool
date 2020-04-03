import json
import logging
import os
import requests

from datetime import datetime, date
from django.conf import settings
from django.core.cache import cache
from django.forms.models import model_to_dict
from mohawk import Sender
from requests.exceptions import RequestException
from rest_framework import status

import app.enquiries.ref_data as ref_data
from app.enquiries.utils import get_oauth_payload


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


def dh_request(
    request,
    access_token,
    method,
    url,
    payload,
    request_headers=None,
    params=None,
    timeout=15,
):
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
        # Extract access token
        if not access_token:
            session = get_oauth_payload(request)
            access_token = session["access_token"] if session else 'invalid-token'

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    params = params if params else {}

    try:
        if method == "GET":
            response = requests.get(
                url, headers=headers, params=params, timeout=timeout
            )
        elif method == "POST":
            response = requests.post(
                url, headers=headers, json=payload, timeout=timeout
            )
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
        logging.error(
            f"Error fetching Data Hub metadata for endpoints: {metadata['failed']}"
        )

    return metadata


def dh_fetch_metadata(cache_key="metadata", expiry_secs=60 * 60):
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


def dh_get_user_details(request, access_token):
    """ Gets the currently logged in user details """

    url = settings.DATA_HUB_WHOAMI_URL

    response = dh_request(request, access_token, "GET", url, {})
    if not response.ok:
        return None, response.json()

    return response.json(), None


def dh_company_search(request, access_token, company_name):
    """
    Peforms a Company name search using Data hub API.

    Returns list of subset of fields for each company found
    """
    companies = []
    url = settings.DATA_HUB_COMPANY_SEARCH_URL
    payload = {"name": company_name}

    response = dh_request(request, access_token, "POST", url, payload)

    # It is not an error for us if the request fails, this can happen if the
    # Access token is invalid, consider that there are no matches however
    # user is notified of the error to take appropriate action
    if not response.ok:
        return companies, response.json()

    for company in response.json()["results"]:
        address = company["address"]
        companies.append(
            {
                "datahub_id": company["id"],
                "name": company["name"],
                "company_number": company["company_number"],
                "duns_number": company["duns_number"],
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


def dh_contact_search(request, access_token, contact_name, company_id):
    """
    Peforms a Contact name search using Data hub API.

    Returns list of subset of fields for each contact found
    """
    contacts = []
    url = settings.DATA_HUB_CONTACT_SEARCH_URL
    payload = {"name": contact_name, "company": [company_id]}

    response = dh_request(request, access_token, "POST", url, payload)

    if not response.ok:
        return contacts, response.json()

    contacts = [
        {
            "datahub_id": contact["id"],
            "first_name": contact["first_name"],
            "last_name": contact["last_name"],
            "job_title": contact["job_title"],
            "email": contact["email"],
            "phone": contact["telephone_number"],
        }
        for contact in response.json()["results"]
    ]

    return contacts, None


def dh_contact_create(request, access_token, enquirer, company_id, primary=False):
    """
    Create a contact and associate with the given Company Id.

    Returns created contact and error if any
    """
    url = settings.DATA_HUB_CONTACT_CREATE_URL
    enquirer = enquirer.enquirer
    payload = {
        "first_name": enquirer.first_name,
        "last_name": enquirer.last_name,
        "job_title": enquirer.job_title,
        "company": company_id,
        "primary": primary,
        "telephone_countrycode": enquirer.phone_country_code,
        "telephone_number": enquirer.phone,
        "email": enquirer.email,
        "address_same_as_company": True,
    }

    response = dh_request(request, access_token, "POST", url, payload)
    if not response.ok:
        return None, response.json()

    return response.json(), None


def dh_adviser_search(request, access_token, adviser_name):
    """
    Peforms an Adviser search using Data hub API.

    Returns list of subset of fields for each Adviser found
    """
    advisers = []
    url = f"{settings.DATA_HUB_ADVISER_SEARCH_URL}"
    params = {"autocomplete": adviser_name}

    response = dh_request(request, access_token, "GET", url, {}, params=params)
    if not response.ok:
        return advisers, response.json()

    advisers = [
        {
            "datahub_id": adviser["id"],
            "name": adviser["first_name"],
            "is_active": adviser["is_active"],
        }
        for adviser in response.json()["results"]
    ]

    return advisers, None


def get_dh_id(metadata_items, name):
    item = list(filter(lambda x: x["name"] == name, metadata_items))
    assert len(item) == 1
    return item[0]["id"]


def dh_enquiry_readiness(request, access_token, enquiry):
    """
    Check whether the given enquiry is ready to be submitted to Data Hub

    Criteria is that the company should exist in Data Hub, crm is valid user,
    given user is available etc

    Returns json response with error description.
    """
    response = {"errors": []}

    # Allow creating of investments only if Company exists on DH
    if not enquiry.dh_company_id:
        response["errors"].append(
            {"company": f"{enquiry.company_name} doesn't exist in Data Hub"}
        )
        return response

    # Same enquiry cannot be submitted if it is already done once
    if (
        enquiry.date_added_to_datahub
        or enquiry.datahub_project_status != ref_data.DatahubProjectStatus.DEFAULT
    ):
        prev_submission_date = (
            enquiry.date_added_to_datahub.strftime("%d %B %Y")
            if enquiry.date_added_to_datahub
            else "----"
        )
        stage = enquiry.get_datahub_project_status_display()
        response["errors"].append(
            {
                "enquiry": f"Enquiry can only be submitted once,"
                f" previously submitted on {prev_submission_date}, stage {stage}"
            }
        )
        return response

    enquiry_dict = model_to_dict(enquiry)
    empty_values = False
    for field in [
        "crm",
        "project_name",
        "project_description",
        "anonymised_project_description",
        "estimated_land_date",
    ]:
        if not enquiry_dict[field]:
            response["errors"].append(
                {field: "This value is required, should not be empty"}
            )
            empty_values = True

    if empty_values:
        return response

    if enquiry.investment_type == "DEFAULT":
        response["errors"].append(
            {"investment_type": "Please select investment type, it cannot be empty"}
        )
        return response

    advisers, error = dh_adviser_search(request, access_token, enquiry.crm)
    if error:
        response["errors"].append({"adviser_search": error})
        return response

    if not advisers:
        response["errors"].append({"adviser": f"CRM {enquiry.crm} not found"})
        return response

    response["adviser"] = advisers[0]["datahub_id"]

    return response


def prepare_dh_payload(
    enquiry, dh_metadata, company_id, contact_id, adviser_id, crm_id
):
    """ Prepares the payload for investment create request """

    payload = {}
    payload["name"] = enquiry.company_name
    payload["investor_company"] = company_id
    payload["description"] = enquiry.project_description
    payload["anonymous_description"] = enquiry.anonymised_project_description
    payload["estimated_land_date"] = ""
    if enquiry.estimated_land_date:
        payload["estimated_land_date"] = enquiry.estimated_land_date.isoformat()
    payload["investment_type"] = get_dh_id(
        dh_metadata["investment-type"], ref_data.DATA_HUB_INVESTMENT_TYPE_FDI
    )
    payload["fdi_type"] = map_to_datahub_id(
        enquiry.get_investment_type_display(), dh_metadata, "fdi-type"
    )
    payload["stage"] = get_dh_id(
        dh_metadata["investment-project-stage"],
        ref_data.DATA_HUB_PROJECT_STAGE_PROSPECT,
    )
    payload["investor_type"] = map_to_datahub_id(
        enquiry.get_new_existing_investor_display(),
        dh_metadata,
        "investment-investor-type",
    )
    payload["level_of_involvement"] = map_to_datahub_id(
        enquiry.get_investor_involvement_level_display(),
        dh_metadata,
        "investment-involvement",
    )
    payload["specific_programme"] = map_to_datahub_id(
        enquiry.get_specific_investment_programme_display(),
        dh_metadata,
        "investment-specific-programme",
    )
    payload["client_contacts"] = [contact_id]
    payload["client_relationship_manager"] = crm_id
    payload["sector"] = map_to_datahub_id(
        enquiry.get_primary_sector_display(), dh_metadata, "sector"
    )
    # There is a mismatch in the sector data coming from the website vs
    # the metadata in DH, hence bail out if we don't get uuid because of mismatch
    if not payload["sector"]:
        return payload, "sector"

    payload["business_activities"] = [ref_data.DATA_HUB_BUSINESS_ACTIVITIES_SERVICES]
    payload["referral_source_adviser"] = adviser_id
    payload["referral_source_activity"] = get_dh_id(
        dh_metadata["referral-source-activity"],
        ref_data.DATA_HUB_REFERRAL_SOURCE_ACTIVITY_WEBSITE,
    )
    payload["referral_source_activity_website"] = get_dh_id(
        dh_metadata["referral-source-website"],
        ref_data.DATA_HUB_REFERRAL_SOURCE_WEBSITE,
    )

    return payload, None


def dh_investment_create(request, enquiry, metadata=None):
    """
    Creates an Investment in Data Hub using the data from the given Enquiry obj.

    Investment is only created if the Company corresponding to the Enquiry exists
    in DH otherwise error is returned.
    Enquirer details are added to the list of contacts for this company.
    If this is the only contact then it will be made primary.
    """

    # Return a list of errors to be displayed in UI
    response = {"errors": []}

    # Extract access token
    session = get_oauth_payload(request)
    access_token = session["access_token"]

    # check if the user is available in Data Hub
    user_details, error = dh_get_user_details(request, access_token)
    if error:
        response["errors"].append({"referral_advisor": error})
        return response

    dh_status = dh_enquiry_readiness(request, access_token, enquiry)
    if dh_status["errors"]:
        response["errors"].extend(dh_status["errors"])
        return response

    try:
        dh_metadata = dh_fetch_metadata()
    except Exception as e:
        response["errors"].append({"metadata": "Error fetching metadata"})
        return response

    company_id = enquiry.dh_company_id
    # Create a contact for this company
    # If a contact already exists then make the new contact as secondary
    full_name = f"{enquiry.enquirer.first_name} {enquiry.enquirer.last_name}"
    existing_contacts, error = dh_contact_search(
        request, access_token, full_name, company_id
    )
    if error:
        response["errors"].append({"contact_search": error})
        return response

    primary = not existing_contacts
    contact_response, error = dh_contact_create(
        request, access_token, enquiry, company_id, primary=primary
    )
    if error:
        response["errors"].append({"contact_create": error})
        return response

    contact_id = contact_response["id"]
    referral_adviser = user_details["id"]
    crm_id = dh_status["adviser"]

    url = settings.DATA_HUB_INVESTMENT_CREATE_URL
    payload, error_key = prepare_dh_payload(
        enquiry, dh_metadata, company_id, contact_id, referral_adviser, crm_id
    )
    if error_key:
        response["errors"].append({error_key: "Reference data mismatch in Data Hub"})
        return response

    try:
        result = dh_request(request, access_token, "POST", url, payload)
        response["result"] = result.json()
    except Exception as e:
        response["errors"].append(
            {"investment_create": f"Error creating investment, {str(e)}"}
        )
        return response

    if result.ok:
        enquiry.datahub_project_status = ref_data.DatahubProjectStatus.PROSPECT
        enquiry.date_added_to_datahub = date.today()
        enquiry.enquiry_stage = ref_data.EnquiryStage.ADDED_TO_DATAHUB
        enquiry.save()

    return response
