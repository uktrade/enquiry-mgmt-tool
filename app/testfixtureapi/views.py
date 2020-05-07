from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View


class ResetFixturesView(View):
    def post(self, request):
        if settings.ALLOW_TEST_FIXTURE_API_URLS != True:
            return HttpResponseNotFound()
        return HttpResponse(status=201)
