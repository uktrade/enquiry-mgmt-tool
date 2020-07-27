from django.urls import reverse

import app.enquiries.tests.utils as test_utils
from app.settings import common

def test_correct_middleware_exists():
  assert common.MIDDLEWARE == [
    'django.middleware.security.SecurityMiddleware',
    'app.middleware.add_cache_control_header_middleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

def test_security_settings_on():
  assert common.SECURE_BROWSER_XSS_FILTER == True

class CustomMiddlewareTestCase(test_utils.BaseEnquiryTestCase):
  def setUp(self):
      super().setUp()

  def test_custom_cache_control_middleware(self):
    """
    Tests that the custom middleware add_cache_control_header_middleware
    adds the correct cache_control header to a response.
    """
    headers = {"HTTP_CONTENT_TYPE": "text/html", "HTTP_ACCEPT": "text/html"}
    response = self.client.get(reverse("index"), **headers)
    assert response["Cache-Control"] == 'max-age=0, no-cache, no-store, must-revalidate, private'
