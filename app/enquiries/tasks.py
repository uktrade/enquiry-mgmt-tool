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

FETCH_INTERVAL_HOURS = f"*/{settings.DATA_HUB_METADATA_FETCH_INTERVAL}"

@periodic_task(
    run_every=(crontab(hour=FETCH_INTERVAL_HOURS)),
    name="refresh_datahub_metadata",
    ignore_result=True,
)
def refresh_datahub_metadata(redis_host="redis", key="metadata"):

    with Redis(host=redis_host) as rds:
        try:
            rds.ping()

            dh_metadata = dh_fetch_metadata()
            rds.set(key, json.dumps(dh_metadata))
            logging.info(f"Data Hub metadata last refreshed at {datetime.now()}")
        except ConnectionError:
            logging.error("Error connecting to Redis backend, cannot fetch metadata")
