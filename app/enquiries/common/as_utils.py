import json
import logging
import mohawk
import requests

from bs4 import BeautifulSoup
from django.db import transaction
from django.conf import settings

import app.enquiries.ref_data as ref_data
from app.enquiries.models import Enquiry, Enquirer, ReceivedEnquiryCursor, FailedEnquiry


def great_ui_sector_rtt_mapping(value):
    """
    Sector data in the website is different from that in dit-sectors reference,
    so we first check if it is in standard reference data otherwise map it to
    our reference data. If not found anywhere use default value.
    """
    rtt_reference = [value for choice in ref_data.PrimarySector.choices if choice[0] == value]
    if rtt_reference:
        return rtt_reference[0]

    mapping = {
        "ADVANCED_MANUFACTURING": ref_data.PrimarySector.DEFAULT.value,
        "AGRICULTURE_HORTICULTURE_AND_FISHERIES": ref_data.PrimarySector.AGRICULTURE.value,
        "EDUCATION_AND_TRAINING": ref_data.PrimarySector.EDUCATION.value,
        "FINANCIAL_AND_PROFESSIONAL_SERVICES": ref_data.PrimarySector.FINANCIAL.value,
        "FOOD_AND_DRINK": ref_data.PrimarySector.FOOD.value,
        "HEALTHCARE_AND_MEDICAL": ref_data.PrimarySector.HEALTHCARE.value,
    }

    return mapping.get(value, ref_data.PrimarySector.DEFAULT.value)


def map_enquiry_data_to_instance(data):
    """
    This function maps the investment enquiry data received from the via website
    to internal database fields so that new Enquiry instances can be created.
    Because the form processing is done in a different place the reference data
    used is not consistent and there are slight mismatches hence this mapping is required.
    """
    enquiry = {}

    call_request_mapping = {
        "in the morning": ref_data.RequestForCall.YES_MORNING,
        "in the afternoon": ref_data.RequestForCall.YES_AFTERNOON,
    }
    investment_readiness = {
        "I’m convinced and want to talk to someone about my plans.": ref_data.InvestmentReadiness.CONVINCED,
        "The UK is on my shortlist. How can the Department for International Trade help me?": ref_data.InvestmentReadiness.SHORTLIST,
        "I’m still exploring where to expand my business and would like to know more about the UK’s offer.": ref_data.InvestmentReadiness.EXPLORING,
        "I’m not yet ready to invest. Keep me informed.": ref_data.InvestmentReadiness.NOT_READY,
    }

    how_did_you_hear = {
        "Press ad (newspaper/trade publication)": ref_data.HowDidTheyHear.PRESS_AD,
        "Outdoor ad/billboard": ref_data.HowDidTheyHear.OUTDOOR_AD,
        "LinkedIn": ref_data.HowDidTheyHear.LINKEDIN,
        "Other social media (e.g. Twitter/Facebook)": ref_data.HowDidTheyHear.SOCIAL_MEDIA,
        "Internet search": ref_data.HowDidTheyHear.INTERNET_SEARCH,
        "Other": ref_data.HowDidTheyHear.OTHER,
    }

    enquiry["company_name"] = data["Company name"]
    enquiry["website"] = data["Company website"]
    enquiry["company_hq_address"] = data["Company HQ address"]
    enquiry["country"] = data["Country"]
    # TODO: map to the correct sector values
    # The reference data values are different from ours so we need to map them
    # A new function required to perform the mapping or better approach is to
    # use directory-constants directly
    enquiry["primary_sector"] = great_ui_sector_rtt_mapping(data["Industry"])
    value = data[
        "Which of these best describes how you feel about expanding to the UK?"
    ]
    enquiry["investment_readiness"] = investment_readiness.get(
        value, ref_data.InvestmentReadiness.DEFAULT
    )
    enquiry["enquiry_text"] = data["Tell us about your investment"]
    value = data.get("How did you hear about us?")
    if value:
        enquiry["how_they_heard_dit"] = how_did_you_hear.get(
            value, ref_data.HowDidTheyHear.DEFAULT
        )
    else:
        enquiry["how_they_heard_dit"] = ref_data.HowDidTheyHear.DEFAULT

    enquiry["enquirer"] = {}
    enquiry["enquirer"]["first_name"] = data["Given name"]
    enquiry["enquirer"]["last_name"] = data["Family name"]
    enquiry["enquirer"]["job_title"] = data["Job title"]
    if data.get("Email address"):
        email = data["Email address"]
    elif data.get("Work email address"):
        email = data["Work email address"]
    enquiry["enquirer"]["email"] = email
    enquiry["enquirer"]["phone"] = data["Phone number"]
    true_or_false = lambda value: True if value == "True" else False
    email_consent = true_or_false(
        data.get("I would like to be contacted by email", "False")
    )
    phone_consent = true_or_false(
        data.get("I would like to be contacted by telephone", "False")
    )
    enquiry["enquirer"]["email_consent"] = email_consent
    enquiry["enquirer"]["phone_consent"] = phone_consent

    value = data.get("When should we call you?")
    if value:
        enquiry["enquirer"]["request_for_call"] = call_request_mapping.get(
            value, ref_data.RequestForCall.DEFAULT
        )
    else:
        enquiry["enquirer"]["request_for_call"] = ref_data.RequestForCall.DEFAULT

    return enquiry


def parse_enquiry_email(submission):
    """
    Parses email body in the submission and returns Enquiry related fields.
    This can be used to create an Enquiry.
    """
    enquiry_data = {}

    body = submission["_source"]["object"][settings.ACTIVITY_STREAM_ENQUIRY_DATA_OBJ][
        "html_body"
    ]
    if not body:
        return enquiry_data

    soup = BeautifulSoup(body, features="lxml")
    table_div = soup.find("div", {"class": "form-table"})
    table = table_div.find("table")

    for tr in table.findAll("tr"):
        row = [d.text for d in tr.findAll("td")]
        enquiry_data[row[0].strip()] = row[1].strip()

    """
    The query parameters are not sufficient to filter investment enquiries
    hence using url as additional filter but some of the other enquiries share
    the same url hence additionally look for specified keys to filter data
    """
    if not (
        set(["Given name", "Job title", "Company HQ address"])
        <= set(enquiry_data.keys())
    ):
        return None

    # map the data to Enquiry model fields
    enquiry = map_enquiry_data_to_instance(enquiry_data)

    return enquiry


def hawk_request(method, url, key_id, secret_key, body):
    header = mohawk.Sender(
        {"id": key_id, "key": secret_key, "algorithm": "sha256"},
        url,
        method,
        content_type="application/json",
        content=body,
    ).request_header

    response = requests.request(
        method,
        url,
        data=body,
        headers={"Authorization": header, "Content-Type": "application/json",},
    )
    return response


def get_new_investment_enquiries(last_cursor=None, max_size=100):
    """
    Helper function to pull new investment enquiries from AS.

    last_cursor indicates the last enquiry fetched (index and id).
    This is used to fetch next set of results when this is invoked again.
    """

    key_id = settings.ACTIVITY_STREAM_KEY_ID
    secret_key = settings.ACTIVITY_STREAM_KEY
    url = settings.ACTIVITY_STREAM_SEARCH_URL
    query = {
        "size": max_size,
        "query": {
            "bool": {
                "filter": [
                    {
                        "term": {
                            settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY1: settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE1
                        }
                    },
                    {
                        "term": {
                            settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2: settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2
                        }
                    },
                ]
            }
        },
        "sort": [{"published": "asc"}, {"id": "asc"}],
    }

    if last_cursor:
        query["search_after"] = [last_cursor.index, last_cursor.object_id]

    response = hawk_request("GET", url, key_id, secret_key, json.dumps(query))
    if not response.ok:
        logging.error(f"Error running query on Activity stream, {response.json()}")
        return None

    response = response.json()

    # url field in the object is not part of search mapping.
    # The above query returns trade related enquiries also hence filter
    # investment related using the url field
    target_url = settings.ACTIVITY_STREAM_SEARCH_TARGET_URL
    enquiries = list(
        filter(
            lambda x: x["_source"]["object"]["url"] == target_url,
            response["hits"]["hits"],
        )
    )

    return enquiries


def fetch_and_process_enquiries():
    """
    Fetches new enquiries from AS and creates new instances in the database
    """

    last_cursor = ReceivedEnquiryCursor.objects.last()

    enquiries = get_new_investment_enquiries(last_cursor, max_size=20)
    if not enquiries:
        return

    logging.info(f"Total number of enquiries retrieved: {len(enquiries)}")

    valid_count = 0
    for item in enquiries:
        enquiry = parse_enquiry_email(item)
        if not enquiry:
            continue

        with transaction.atomic():
            enquirer = enquiry.pop("enquirer")
            enquirer_instance = Enquirer.objects.create(**enquirer)
            enquiry_obj = Enquiry.objects.create(**enquiry, enquirer=enquirer_instance)
            logging.info(
                f"Enquiry ({enquiry_obj.id}) created for the company {enquiry_obj.company_name}"
            )
            valid_count += 1

    last_obj = enquiries[-1]
    ReceivedEnquiryCursor.objects.create(
        index=last_obj["sort"][0], object_id=last_obj["sort"][1]
    )
    logging.info(f"Number of valid enquiries found: {valid_count}/{len(enquiries)}")
