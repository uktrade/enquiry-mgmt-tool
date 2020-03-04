import json
import os
import requests

from django.conf import settings
from mohawk import Sender
from rest_framework import status


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
            meta_url, headers={"Authorization": sender.request_header},
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
