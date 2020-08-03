from django.urls import path

from app.testfixtureapi.views import TestFixtureResetView


app_name = "testfixtureapi"
urlpatterns = [
    path("reset-fixtures/", TestFixtureResetView.as_view(), name="reset-fixtures",),
]
