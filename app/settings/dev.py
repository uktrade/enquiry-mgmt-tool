from app.settings.common import *

ROOT_URLCONF = 'app.test_urls'

if env('ALLOW_TEST_FIXTURE_API_URLS', default=None) == 'allow':
    # For obvious reasons, never EVER set this to True in non-test environments
    ALLOW_TEST_FIXTURE_API_URLS = True
else:
    ALLOW_TEST_FIXTURE_API_URLS = False
