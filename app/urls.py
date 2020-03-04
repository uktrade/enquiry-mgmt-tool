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
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from app.enquiries import views


urlpatterns = [
    path('', views.EnquiryList.as_view(), name="enquiry-list"),
    path('admin/', admin.site.urls),
    path('api/v1/enquiries/', views.EnquiryList.as_view(), name="enquiry-list"),
    path('api/v1/enquiries/add', views.EnquiryAdd.as_view(), name="enquiry-add"),
    path('api/v1/enquiries/<int:pk>/', views.EnquiryDetail.as_view(), name="enquiry-detail"),
    path('api/v1/enquiries/<int:pk>/edit', views.EnquiryDetail.as_view(), name="enquiry-edit"),
]
