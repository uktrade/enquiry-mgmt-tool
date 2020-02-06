from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from enquiries import models



class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enquiry
        fields = "__all__"
