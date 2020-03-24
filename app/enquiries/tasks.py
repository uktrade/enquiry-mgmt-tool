import json
import logging

from celery.task import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import datetime
from django.conf import settings
from redis import Redis
from redis.exceptions import ConnectionError

from app.enquiries.common.datahub_utils import dh_fetch_metadata

FETCH_INTERVAL_HOURS = f"*/{settings.DATA_HUB_METADATA_FETCH_INTERVAL_HOURS}"


@periodic_task(
    run_every=(crontab(hour=FETCH_INTERVAL_HOURS, minute="0")),
    name="refresh_datahub_metadata",
    ignore_result=True,
)
def refresh_datahub_metadata():
    """ Periodically refreshes metadata in cache """

    # set expiry few minutes before next refresh so that we
    # ensure refresh fetch data again
    expiry_secs = settings.DATA_HUB_METADATA_FETCH_INTERVAL_HOURS * 60 * 60 - (5 * 60)
    dh_metadata = dh_fetch_metadata(expiry_secs=expiry_secs)
    logging.info(f"Data Hub metadata last refreshed at {datetime.now()}")
