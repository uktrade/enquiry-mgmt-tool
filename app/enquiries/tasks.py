import logging

from datetime import datetime
from django.conf import settings

from app.enquiries.celery import app
from app.enquiries.common.as_utils import fetch_and_process_enquiries
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
