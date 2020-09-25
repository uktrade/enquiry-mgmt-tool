import logging

from datetime import datetime
from django.conf import settings

from app.enquiries.celery import app
from app.enquiries.common.datahub_utils import dh_fetch_metadata
from app.enquiries.common.as_utils import fetch_and_process_enquiries
from app.enquiries.common.email_campaign_utils import (
    process_latest_enquiries,
    process_second_qualifications,
    process_engaged_enquiries,
)
from app.enquiries.utils import mark_non_responsive_enquiries

FETCH_INTERVAL_HOURS = f"*/{settings.DATA_HUB_METADATA_FETCH_INTERVAL_HOURS}"


@app.task(name="refresh_datahub_metadata")
def refresh_datahub_metadata():
    """Periodically refreshes |data-hub-api|_ metadata in cache """

    # set expiry a few minutes before next refresh so that we
    # ensure refresh fetches data again
    expiry_secs = settings.DATA_HUB_METADATA_FETCH_INTERVAL_HOURS * 60 * 60 - (5 * 60)
    dh_fetch_metadata(expiry_secs=expiry_secs)
    logging.info(f"Data Hub metadata last refreshed at {datetime.now()}")


@app.task(name="fetch_new_enquiries")
def fetch_new_enquiries():
    """Periodically fetches new `investment enquiries` from |activity-stream|_"""

    fetch_and_process_enquiries()
    logging.info(f"New enquiries last retrieved at {datetime.now()}")


@app.task(name="handle_non_responsives")
def handle_non_responsives():
    """ Periodically fetch and handle non responsive enquiries """
    process_latest_enquiries()
    logging.info("Fetched non responsive enquiries %s", datetime.now())

    
@app.task(name="update_stage_stale_enquiries")
def update_stage_stale_enquiries():
    """ Periodically changes older enquiries from 'Awaiting Response' to 'Non-responsive' """

    mark_non_responsive_enquiries(expiry_weeks=settings.ENQUIRY_RESPONSIVENESS_PERIOD_WEEKS)
    logging.info(f"Older enquiries marked as 'Non-responsive' at {datetime.now()}")
