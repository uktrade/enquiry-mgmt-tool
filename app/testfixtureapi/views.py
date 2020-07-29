from django.conf import settings
from django.contrib.auth import login
from django.core.management import call_command
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries.models import (
    Enquirer,
    Enquiry,
    Owner,
)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Stop CSRF checks.

    The view we are implementing needs to be CSRF exempt. While DRF
    avoids CSRF checks for anonymous calls it enforces them for non-read
    calls made by logged in API clients. Subsequent calls to the same
    reset URL may be made with a session cookie in the header and so
    DRF will enforce CSRF (unless we stop it).

    """

    def enforce_csrf(self, request):
        return


class TestFixtureResetView(APIView):
    """
    Reset db to a known state; create and log in a seed user.

    This view is to facilitate End to End testing. It is only enabled under
    safe circumstances - see "Allowing for Fixture Reset during e2e tests"
    in README.md

    POST to this view with a payload which is a single JSON object containing
    the following properties:
        - username
        - first_name
        - last_name
        - email

    (Content-Type must be 'application/json')

    The database will have its Enquiry, Enquirer and Owner objects removed and
    reset to the state in the fixtures files. In addition a 'seed user' will be
    created according to the data supplied in your payload and that user will
    be automatically logged in (to simplify the e2e testing cycle).

    """

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, *args, **kwargs):
        if not settings.ALLOW_TEST_FIXTURE_SETUP:
            return Response(status=status.HTTP_404_NOT_FOUND)
        seed_user_data = {
            "username": request.data["username"],
            "first_name": request.data["first_name"],
            "last_name": request.data["last_name"],
            "email": request.data["email"],
        }
        Enquiry.objects.all().delete()
        Enquirer.objects.all().delete()
        Owner.objects.all().delete()
        call_command(
            "loaddata", "app/enquiries/fixtures/test_users.json", app_label="enquiries",
        )
        call_command(
            "loaddata", "app/enquiries/fixtures/test_enquiries.json", app_label="enquiries",
        )
        seed_user = Owner.objects.create(**seed_user_data)
        login(
            request, seed_user, backend="django.contrib.auth.backends.ModelBackend",
        )
        return Response(status=status.HTTP_201_CREATED)
