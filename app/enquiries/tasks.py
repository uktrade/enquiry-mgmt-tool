import logging

from datetime import datetime
from django.conf import settings

from app.enquiries.celery import app
from app.enquiries.common.as_utils import fetch_and_process_enquiries
from app.enquiries.common.email_campaign_utils import (
    process_latest_enquiries,
    process_second_qualifications,
    process_engaged_enquiries,
)
from app.enquiries.utils import mark_non_responsive_enquiries


@app.task(name="fetch_new_enquiries")
def fetch_new_enquiries():
    """Periodically fetches new `investment enquiries` from |activity-stream|_"""

    fetch_and_process_enquiries()
    logging.info(f"New enquiries last retrieved at {datetime.now()}")


@app.task(name="update_stage_stale_enquiries")
def update_stage_stale_enquiries():
    """ Periodically changes older enquiries from 'Awaiting Response' to 'Non-responsive' """

    mark_non_responsive_enquiries(expiry_weeks=settings.ENQUIRY_RESPONSIVENESS_PERIOD_WEEKS)
    logging.info(f"Older enquiries marked as 'Non-responsive' at {datetime.now()}")


@app.task(name="handle_non_responsives")
def handle_non_responsives():
    """ Periodically fetch and handle non responsive enquiries """
    process_latest_enquiries()
    logging.info("Fetched non responsive enquiries %s", datetime.now())


@app.task(name="handle_second_qualifications")
def handle_second_qualifications():
    """ Periodically fetch and handle 2nd qualification submissions """
    process_second_qualifications()
    logging.info("Fetched 2nd qualification submissions %s", datetime.now())


@app.task(name="handle_engaged_leads")
def handle_exit_criteria_enquiries():
    """ Periodically fetch and handle enquirers marked as  sent-to-post"""
    process_engaged_enquiries()
    logging.info("Fetched completed enquiries %s", datetime.now())
