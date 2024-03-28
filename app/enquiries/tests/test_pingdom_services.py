from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase
from redis import RedisError

from app.enquiries.pingdom.services import CheckCelery, CheckDatabase, CheckRedis


class PingdomServicesTestCase(TestCase):
    def test_check_database_success(self):
        check_database = CheckDatabase()
        result = check_database.check()
        assert check_database.name == "database"
        assert result == (True, "")

    def test_check_database_failure(self):
        check_database = CheckDatabase()
        with patch(
            'app.enquiries.models.Enquiry.objects.exists',
            side_effect=DatabaseError('No database'),
        ):
            result = check_database.check()

        assert result == (False, "Pingdom check Database: No database")

    def test_check_celery_success(self):
        check_celery = CheckCelery()
        with patch(
            'app.enquiries.celery.app.control.inspect.stats',
            return_value=[{}]
        ):
            result = check_celery.check()
        assert check_celery.name == "celery"
        assert result == (True, "")

    def test_check_celery_failure(self):
        check_celery = CheckCelery()
        with patch(
            'app.enquiries.celery.app.control.inspect.stats',
            return_value=None
        ):
            result = check_celery.check()

        assert result == (False, "Pingdom check Celery: Celery is not running")

    def test_check_redis_success(self):
        check_redis = CheckRedis()
        with patch(
            'redis.Redis.ping',
            return_value=True,
        ):
            result = check_redis.check()
        assert check_redis.name == "redis"
        assert result == (True, "")

    def test_check_redis_failure(self):
        check_redis = CheckRedis()
        with patch(
            'redis.Redis.ping',
            side_effect=RedisError("Redis error"),
        ):
            result = check_redis.check()

        assert result == (False, "Pingdom check Redis: Redis error")
