from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View

from app.enquiries.models import (
    Enquirer,
    Enquiry,
    Owner,
)

class ResetFixturesView(View):
    def post(self, request):
        if settings.ALLOW_TEST_FIXTURE_API_URLS != True:
            return HttpResponseNotFound()
        Enquiry.objects.all().delete()
        Enquirer.objects.all().delete()
        Owner.objects.all().delete()
        call_command(
            'loaddata',
            'app/enquiries/fixtures/test_users.json',
            app_label='enquiries',
        )
        call_command(
            'loaddata',
            'app/enquiries/fixtures/test_enquiries.json',
            app_label='enquiries',
        )
        return HttpResponse(status=201)
