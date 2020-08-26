import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.common")
app = Celery("app")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

DH_METADATA_FETCH_INTERVAL_HOURS = settings.DATA_HUB_METADATA_FETCH_INTERVAL_HOURS
AS_ENQUIRIES_POLL_INTERVAL_MINS = settings.ACTIVITY_STREAM_ENQUIRY_POLL_INTERVAL_MINS
ENQUIRY_STATUS_UPDATE_INTERVAL_DAYS = settings.ENQUIRY_STATUS_UPDATE_INTERVAL_DAYS
ENQUIRY_STATUS_SHOULD_UPDATE = settings.ENQUIRY_STATUS_SHOULD_UPDATE

app.conf.beat_schedule = {
    "refresh-datahub-metadata": {
        "task": "refresh_datahub_metadata",
        "schedule": crontab(minute="0", hour=f"*/{DH_METADATA_FETCH_INTERVAL_HOURS}"),
    },
    "fetch-new-enquiries": {
        "task": "fetch_new_enquiries",
        "schedule": crontab(minute=f"*/{AS_ENQUIRIES_POLL_INTERVAL_MINS}"),
    },
    "update-stage-stale-enquiries": {
        "task": "update_stage_stale_enquiries",
        "schedule": crontab(minute="0", hour="0",
                            day_of_month=f"*/{ENQUIRY_STATUS_UPDATE_INTERVAL_DAYS}"
                            )
    }
} if ENQUIRY_STATUS_SHOULD_UPDATE else {
    "refresh-datahub-metadata": {
        "task": "refresh_datahub_metadata",
        "schedule": crontab(minute="0", hour=f"*/{DH_METADATA_FETCH_INTERVAL_HOURS}"),
    },
    "fetch-new-enquiries": {
        "task": "fetch_new_enquiries",
        "schedule": crontab(minute=f"*/{AS_ENQUIRIES_POLL_INTERVAL_MINS}"),
    }
}
