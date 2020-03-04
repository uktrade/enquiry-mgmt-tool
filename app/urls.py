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
from django.urls import path
from django.views.generic import TemplateView

import app.enquiries.ref_data as ref_data
from app.enquiries import views
from app.enquiries.common.datahub_utils import dh_fetch_metadata, map_to_datahub_id


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("admin/", admin.site.urls),
    path("enquiries/", views.EnquiryListView.as_view(), name="enquiry-list"),
]


print("Enquiries app is ready, fetch metadata from Data Hub...")
settings.dh_metadata = dh_fetch_metadata()
