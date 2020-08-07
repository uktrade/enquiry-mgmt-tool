import logging

from datetime import datetime
from django.conf import settings

from app.enquiries.celery import app
from app.enquiries.common.datahub_utils import dh_fetch_metadata
from app.enquiries.common.as_utils import fetch_and_process_enquiries

FETCH_INTERVAL_HOURS = f"*/{settings.DATA_HUB_METADATA_FETCH_INTERVAL_HOURS}"


@app.task(name="refresh_datahub_metadata")
def refresh_datahub_metadata():
    """ Periodically refreshes metadata in cache """

    # set expiry a few minutes before next refresh so that we
    # ensure refresh fetches data again
    expiry_secs = settings.DATA_HUB_METADATA_FETCH_INTERVAL_HOURS * 60 * 60 - (5 * 60)
    dh_fetch_metadata(expiry_secs=expiry_secs)
    logging.info(f"Data Hub metadata last refreshed at {datetime.now()}")


@app.task(name="fetch_new_enquiries")
def fetch_new_enquiries():
    """ Periodically fetches new investment enquiries from AS """

    fetch_and_process_enquiries()
    logging.info(f"New enquiries last retrieved at {datetime.now()}")
