from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse
from rest_framework import status

from app.enquiries.models import Enquiry


PINGDOM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<pingdom_http_custom_check>
    <status>{status}</status>
</pingdom_http_custom_check>\n
<!-- {comment} -->\n"""


def ping(request):
    """
    Ping view for Service health checks

    Service is healthy if we can query database
    """

    comment = ""
    db_conn = connections["default"]

    try:
        db_status = db_conn.cursor()
        Enquiry.objects.all().exists()
        http_status = status.HTTP_200_OK
        comment = "OK"
    except OperationalError:
        db_status = False
        enquiries_exist = False
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    return HttpResponse(
        PINGDOM_TEMPLATE.format(status="OK" if db_status else "ERROR", comment=comment),
        status=http_status,
        content_type="text/xml",
    )
