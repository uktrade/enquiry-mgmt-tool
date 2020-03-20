import json
import logging
import mohawk
import requests

from django.conf import settings

from app.enquiries.models import ReceivedEnquiryCursor


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

    last_cursor indicates the last enquiry fetched (timestamp and id).
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
        query["search_after"] = [last_cursor.timestamp, last_cursor.object_id]

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
