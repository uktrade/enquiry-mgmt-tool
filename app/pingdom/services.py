from django.conf import settings
from django.db import DatabaseError
from redis import Redis

from app.enquiries.celery import app as celery_app
from app.enquiries.models import Enquiry


class CheckDatabase:
    """Check the database is up and running."""

    name = "database"

    def check(self):
        """Perform the check."""
        try:
            Enquiry.objects.exists()
            return True, ""
        except DatabaseError as exception:
            return False, f"Pingdom check Database: {exception}"


class CheckCelery:
    name = "celery"

    def check(self):
        try:
            insp = celery_app.control.inspect()
            nodes = insp.stats()
            if not nodes:
                raise Exception("Celery is not running")
            return True, ""
        except Exception as exception:
            return False, f"Pingdom check Celery: {exception}"


class CheckRedis:
    name = "redis"

    def check(self):
        try:
            redis = Redis.from_url(settings.REDIS_BASE_URL)
            if redis.ping():
                return True, ""
            else:
                return False, "Redis is not connected"
        except Exception as exception:
            return False, f"Pingdom check Redis: {exception}"


services_to_check = (
    CheckDatabase,
    CheckRedis,
)
