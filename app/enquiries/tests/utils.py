from faker import Faker
import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import Client, TestCase

logger = logging.getLogger(__name__)


class BaseEnquiryTestCase(TestCase):
    def setUp(self):
        """
        Sets up test user to authenticate requests.
        If you need to log out for a test remember to log bck in afterwards
        """
        self.faker = Faker()
        self.client = Client()

        self.CREDENTIALS = {"username": "test", "password": "user"}
        self.logged_in = False
        user_model = get_user_model()
        with transaction.atomic():
            # create test user
            self.u = user_model(username=self.CREDENTIALS["username"])
            self.u.set_password(self.CREDENTIALS["password"])
            self.u.save()
        # login
        self.login()

    def tearDown(self):
        with transaction.atomic():
            self.u.delete()

    def login(self):
        self.logged_in = self.client.login(**self.CREDENTIALS)
        logger.info(f"Login response: {self.logged_in}")
        return self.logged_in

    def logout(self):
        self.logged_in = False
        self.client.logout()
        logger.info("Logged out")
