"""enquiry_mgmt_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from app.enquiries import views
from app.enquiries.pingdom.views import ping

urlpatterns = [
    path("", views.EnquiryListView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("enquiry/", views.EnquiryCreateView.as_view(), name="enquiry-create"),
    path(
        "enquiries/template/",
        views.ImportTemplateDownloadView.as_view(),
        name="import-template",
    ),
    path(
        "enquiries/import", views.ImportEnquiriesView.as_view(), name="import-enquiries"
    ),
    path(
        "enquiries/<int:pk>/", views.EnquiryDetailView.as_view(), name="enquiry-detail"
    ),
    path(
        "enquiries/<int:pk>/edit", views.EnquiryEditView.as_view(), name="enquiry-edit"
    ),
    path(
        "enquiries/<int:pk>/company-search",
        views.EnquiryCompanySearchView.as_view(),
        name="enquiry-company-search",
    ),
    path(
        "enquiries/<int:pk>/delete",
        views.EnquiryDeleteView.as_view(),
        name="enquiry-delete",
    ),
    path("pingdom/ping.xml", ping, name="ping"),
    path(
        "dh-adviser-search",
        views.DataHubAdviserSearch.as_view(),
        name="dh-adviser-search",
    ),
    path("api/v1/enquiries", views.APIEnquiries.as_view(), name="api-v1-enquiries"),
]

if settings.FEATURE_FLAGS["ENFORCE_STAFF_SSO_ON"]:
    urlpatterns.append(
        path("auth/", include("authbroker_client.urls")),
    )
