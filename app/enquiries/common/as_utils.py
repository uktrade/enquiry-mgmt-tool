import json
import logging
from datetime import datetime

import mohawk
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import transaction

import app.enquiries.ref_data as ref_data
from app.enquiries import utils
from app.enquiries.common import consent_utils
from app.enquiries.models import Enquirer, Enquiry, ReceivedEnquiryCursor


def great_ui_sector_rtt_mapping(value):
    """
    Resolves the `primary sector` for ``value``.

    Sector data in the website is different from that in `dit-sectors`
    reference, so we first check if it is in standard reference data otherwise
    map it to our reference data. If not found anywhere use default value.

    :param value:
    :type value: str

    :returns: |great|_ `sector`
    :rtype: str
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


def via_enquiry_to_enquiry_kwargs(data):
    """
    Converts `enquiry` submitted via email into a dict of `kwargs` for
    :class:`app.enquiries.models.Enquiry`.

    :param data:
    :type data: dict

    :returns:

        A ``dict`` of :class:`app.enquiries.models.Enquiry` constructor
        `kwargs`.
    """
    enquiry = {}

    call_request_mapping = {
        "in the morning": ref_data.RequestForCall.YES_MORNING,
        "in the afternoon": ref_data.RequestForCall.YES_AFTERNOON,
    }
    investment_readiness = {
        "I’m convinced and want to talk to someone about my plans.":
            ref_data.InvestmentReadiness.CONVINCED,
        "The UK is on my shortlist. How can the Department for "
        "Business and Trade help me?":
            ref_data.InvestmentReadiness.SHORTLIST,
        "I’m still exploring where to expand my business and would "
        "like to know more about the UK’s offer.":
            ref_data.InvestmentReadiness.EXPLORING,
        "I’m not yet ready to invest. Keep me informed.":
            ref_data.InvestmentReadiness.NOT_READY,
    }
    enquiry_stage = {
        "New": ref_data.EnquiryStage.NEW,
        "Awaiting response from Investor": ref_data.EnquiryStage.AWAITING_RESPONSE,
        "Engaged in dialogue": ref_data.EnquiryStage.ENGAGED,
        "Non-responsive": ref_data.EnquiryStage.NON_RESPONSIVE,
        "Non-FDI": ref_data.EnquiryStage.NON_FDI,
        "Added to Data Hub": ref_data.EnquiryStage.ADDED_TO_DATAHUB,
        "Sent to Post": ref_data.EnquiryStage.SENT_TO_POST,
        "Post progressing": ref_data.EnquiryStage.POST_PROGRESSING,
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
    enquiry["primary_sector"] = great_ui_sector_rtt_mapping(data["Industry"])
    value = data["Which of these best describes how you feel about expanding to the UK?"]
    enquiry["investment_readiness"] = investment_readiness.get(
        value, ref_data.InvestmentReadiness.DEFAULT
    )
    enquiry["enquiry_stage"] = enquiry_stage.get(value, ref_data.EnquiryStage.NEW)
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
    email_consent = utils.str2bool(
        data.get("I would like to receive additional information by email", "False")
    )
    phone_consent = utils.str2bool(
        data.get("I would like to receive additional information by telephone", "False")
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

    :param submission: The email to be parsed
    :type submission: dict

    :returns:
        The result of :func:`via_enquiry_to_enquiry_kwargs` or ``{}`` or ``None``
    """
    enquiry_data = {}

    body = submission["_source"]["object"][settings.ACTIVITY_STREAM_ENQUIRY_DATA_OBJ]["html_body"]
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
    if not ({"Given name", "Job title", "Company HQ address"} <= enquiry_data.keys()):
        return None

    return via_enquiry_to_enquiry_kwargs(enquiry_data)


def hawk_request(method, url, id_, secret_key, body):
    """
    Makes a :mod:`hawk` request

    :param method: A valid HTTP method
    :type method: str

    :param url: A valid URL
    :type url: str

    :param id_: The ``id`` for the ``credentials`` argument to :class:`mohawk.Sender`
    :type id_: str

    :param secret_key:
        The ``secret_key`` for the ``credentials`` argument to :class:`mohawk.Sender`
    :type secret_key: str

    :param body: A JSON serializable data structure to be sent as the request body

    :returns: :class:`requests.Response`
    """
    header = mohawk.Sender(
        {"id": id_, "key": secret_key, "algorithm": "sha256"},
        url,
        method,
        content_type="application/json",
        content=body,
    ).request_header

    response = requests.request(
        method,
        url,
        data=body,
        headers={"Authorization": header, "Content-Type": "application/json"},
    )
    return response


def get_new_investment_enquiries(last_cursor=None, max_size=100):
    """
    Fetches new investment enquiries from |activity-stream|_.
    The ``ACTIVITY_STREAM_INITIAL_LOAD_DATE`` environmental variable determines
    the initial date from which the data is queried.

    Two emails are sent for every enquiry, one to the user who filled
    out the form and one to enquiries@invest-trade.uk for triage. Both of
    these are present in activity stream. To avoid duplicate enquiries, the
    emails sent to the user are ignored by filtering out emails which
    were sent by noreply@invest.great.gov.uk.

    :param last_cursor:
        Indicates the last enquiry fetched (index and id).
        This is used to fetch next set of results when this is invoked again.
    :type last_cursor: str

    :param max_size: The maximum number of results to fetch
    :type max_size: int

    :returns: JSON-parsed response or ``None`` in case of an error
    """

    key_id = settings.ACTIVITY_STREAM_KEY_ID
    secret_key = settings.ACTIVITY_STREAM_KEY
    url = settings.ACTIVITY_STREAM_SEARCH_URL
    start_date_str = settings.ACTIVITY_STREAM_INITIAL_LOAD_DATE
    start_date = datetime.strptime(start_date_str, "%d-%B-%Y").isoformat()
    query = {
        "size": max_size,
        "query": {
            "bool": {
                "filter": [
                    {"range": {"object.published": {"gte": start_date}}},
                    {
                        "term": {
                            settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY1:
                                settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE1
                        }
                    },
                    {
                        "term": {
                            settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2:
                                settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2
                        }
                    },
                    {
                        "bool": {
                            "must_not": {
                                "term": {"actor.dit:emailAddress": "noreply@invest.great.gov.uk"}
                            }
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
        # FIXME: Throw an error instead of returning None
        logging.error(f"Error running query on Activity stream, {response.json()}")
        return None

    response = response.json()

    # url field in the object is not part of search mapping.
    # The above query returns trade related enquiries also hence filter
    # investment related using the url field
    target_url = settings.ACTIVITY_STREAM_SEARCH_TARGET_URL
    enquiries = list(
        filter(lambda x: x["_source"]["object"]["url"] == target_url, response["hits"]["hits"])
    )

    return enquiries


def fetch_and_process_enquiries():
    """
    Fetches new enquiries from |activity-stream|_ and creates saved
    :class:`app.enquiries.models.Enquiry` instances.
    """

    last_cursor = ReceivedEnquiryCursor.objects.last()

    enquiries = get_new_investment_enquiries(last_cursor, max_size=40)
    if not enquiries:
        return

    logging.info(f"Total number of enquiries retrieved: {len(enquiries)}")

    valid_count = 0
    for item in enquiries:
        enquiry = parse_enquiry_email(item)
        if not enquiry:
            continue

        with transaction.atomic():
            published = item["_source"]["object"]["published"]
            enquirer = enquiry.pop("enquirer")

            consent_utils.create_consent_update_task(data=enquirer)
            enquirer.pop("email_consent")
            enquirer.pop("phone_consent")

            enquirer_instance = Enquirer.objects.create(**enquirer)
            enquiry_obj = Enquiry.objects.create(**enquiry, enquirer=enquirer_instance)
            enquiry_obj.created = published
            enquiry_obj.date_received = published
            enquiry_obj.save()
            logging.info(
                f"""
                Enquiry ({enquiry_obj.id}) created for the company {enquiry_obj.company_name}
                """
            )
            valid_count += 1

    last_obj = enquiries[-1]
    ReceivedEnquiryCursor.objects.create(index=last_obj["sort"][0], object_id=last_obj["sort"][1])
    logging.info(f"Number of valid enquiries found: {valid_count}/{len(enquiries)}")


def get_new_second_qualification_forms(last_datetime=None, max_size=100):
    """
    Fetches new submissions of the second qualification form
    from |activity-stream|_.
    The submissions are fetched from last_datetime onward, or without
    a date filter if not provided.

    :param last_datetime:
        The last time a second qualification form was submitted.
        Subsequent forms will filter after this date. If omited
        all forms will be fetched
    :type last_datetime: datetime

    :param max_size: The maximum number of results to fetch
    :type max_size: int

    :returns: JSON-parsed response or ``None`` in case of an error
    """

    key_id = settings.ACTIVITY_STREAM_KEY_ID
    secret_key = settings.ACTIVITY_STREAM_KEY
    url = settings.ACTIVITY_STREAM_SEARCH_URL
    search_filter = [
        {"range": {"object.published": {"gte": last_datetime.isoformat()}}}
    ] if last_datetime else []
    search_filter += [
        {
            "term": {
                settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY1:
                    settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE1
            }
        },
        {
            "term": {
                settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2:
                    settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2
            }
        },
        {
            "term": {
                settings.ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_NAME:
                    settings.ACTIVITY_STREAM_SECOND_QUALIFICATION_SEARCH_VALUE
            }
        }
    ]

    query = {
        "size": max_size,
        "query": {
            "bool": {
                "filter": search_filter
            }
        },
        "sort": [{"published": "asc"}, {"id": "asc"}],
    }

    response = hawk_request("GET", url, key_id, secret_key, json.dumps(query))
    if not response.ok:
        logging.error(f"Error running query on Activity stream, {response.json()}")
        return None

    response = response.json()
    return response["hits"]["hits"]
