from django.db.utils import OperationalError
from django.http import HttpResponse
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from app.enquiries.models import Enquiry


def ping(request):
    """
    Ping view for Service health checks

    Service is healthy if we can query database
    """

    db_status = False
    try:
        Enquiry.objects.exists()
        db_status = True
    except OperationalError:
        pass

    return HttpResponse(
        "OK" if db_status else "ERROR",
        status=HTTP_200_OK if db_status else HTTP_500_INTERNAL_SERVER_ERROR,
        content_type="text/plain",
    )
