from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TestFixtureResetView(APIView):
    """
    Reset db to a known state.

    This view is to facilitate End to End testing. It is only enabled under
    safe circumstances - see "Allowing for Fixture Reset during e2e tests"
    in README.md.

    """
    def post(self, request, *args, **kwargs):
        if not settings.ALLOW_TEST_FIXTURE_SETUP:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_201_CREATED)
