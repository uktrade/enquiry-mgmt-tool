from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from app.enquiries import models


class EnquirySerializer(WritableNestedModelSerializer):

    class Meta:
        model = models.Enquiry
        fields = "__all__"


class EnquiryDetailSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    owner = serializers.CharField(source="get_owner_display")
    enquiry_stage = serializers.CharField(source="get_enquiry_stage_display")
    investment_readiness = serializers.CharField(source="get_investment_readiness_display")
    quality = serializers.CharField(source="get_quality_display")
    marketing_channel = serializers.CharField(source="get_marketing_channel_display")
    how_they_heard_dit = serializers.CharField(source="get_how_they_heard_dit_display")
    primary_sector = serializers.CharField(source="get_primary_sector_display")
    ist_sector = serializers.CharField(source="get_ist_sector_display")
    country = serializers.CharField(source="get_country_display")
    region = serializers.CharField(source="get_region_display")
    request_for_call = serializers.CharField(source="get_request_for_call_display")
    first_response_channel = serializers.CharField(source="get_first_response_channel_display")
    first_hpo_selection = serializers.CharField(source="get_first_hpo_selection_display")
    second_hpo_selection = serializers.CharField(source="get_second_hpo_selection_display")
    third_hpo_selection = serializers.CharField(source="get_third_hpo_selection_display")
    organisation_type = serializers.CharField(source="get_organisation_type_display")
    investment_type = serializers.CharField(source="get_investment_type_display")
    new_existing_investor = serializers.CharField(source="get_new_existing_investor_display")
    investor_involvement_level = serializers.CharField(source="get_investor_involvement_level_display")
    specific_investment_program = serializers.CharField(source="get_specific_investment_program_display")
    datahub_project_status = serializers.CharField(source="get_datahub_project_status_display")

    class Meta:
        model = models.Enquiry
        fields = "__all__"