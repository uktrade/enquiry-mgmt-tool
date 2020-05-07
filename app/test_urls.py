from django.urls import path, include

from app.urls import urlpatterns


urlpatterns.append(
    path('testfixtureapi/', include('app.testfixtureapi.urls')),
)
