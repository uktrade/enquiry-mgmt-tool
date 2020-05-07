from importlib import reload

from django.test import Client
from django.urls import reverse
from rest_framework import status

RESET_URL = reverse('testfixtureapi:reset-fixtures')


def test_url_not_found_if_not_setup():
    response = Client().post(RESET_URL)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_url_found_if_env_setup(settings):
    settings.ALLOW_TEST_FIXTURE_API_URLS = True
    response = Client().post(RESET_URL)
    assert response.status_code == status.HTTP_201_CREATED
