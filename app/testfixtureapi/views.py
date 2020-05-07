from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.enquiries.models import (
    Enquirer,
    Enquiry,
    Owner,
)

class ResetFixturesView(View):
    """
    Allow for reset of db to 'fixtures' state.

    """
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        Process the request to reset the state.

        """
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
