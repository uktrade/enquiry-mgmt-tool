from django.conf import settings
from django.core.management import call_command
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries.models import (
    Enquirer,
    Enquiry,
    Owner,
)

class TestFixtureResetView(APIView):
    """
    Reset db to a known state.

    This view is to facilitate End to End testing. It is only enabled under
    safe circumstances - see "Allowing for Fixture Reset during e2e tests"
    in README.md.

    The database will have its Enquiry, Enquirer and Owner objects removed and
    reset to the state in the fixtures files.

    """
    def post(self, request, *args, **kwargs):
        if not settings.ALLOW_TEST_FIXTURE_SETUP:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Enquiry.objects.all().delete()
        Enquirer.objects.all().delete()
        Owner.objects.all().delete()
        call_command(
            'loaddata',
            'app/enquiries/fixtures/users.json',
            app_label='enquiries',
        )
        call_command(
            'loaddata',
            'app/enquiries/fixtures/enquiries.json',
            app_label='enquiries',
        )
        return Response(status=status.HTTP_201_CREATED)
