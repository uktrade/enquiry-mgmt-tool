from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from app.enquiries import models

from datetime import timedelta
from datetime import datetime

import app.enquiries.ref_data as ref_data

class OwnerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Owner
        fields = "__all__"

    def get_user(self, obj):
        return obj

class EnquirerDetailSerializer(serializers.ModelSerializer):
    request_for_call = serializers.CharField(source="get_request_for_call_display")
    class Meta:
        model = models.Enquirer
        fields = "__all__"

class EnquirySerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d %B %Y ", read_only=True)
    modified = serializers.DateTimeField(format="%d %B %Y", read_only=True)

    class Meta:
        model = models.Enquiry
        fields = "__all__"


class EnquiryDetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    enquirer = EnquirerDetailSerializer()
    created = serializers.DateTimeField(format="%d %B %Y")
    modified = serializers.DateTimeField(format="%d %B %Y")
    enquiry_stage = serializers.CharField(source="get_enquiry_stage_display")
    investment_readiness = serializers.CharField(source="get_investment_readiness_display")
    quality = serializers.CharField(source="get_quality_display")
    marketing_channel = serializers.CharField(source="get_marketing_channel_display")
    how_they_heard_dit = serializers.CharField(source="get_how_they_heard_dit_display")
    primary_sector = serializers.CharField(source="get_primary_sector_display")
    ist_sector = serializers.CharField(source="get_ist_sector_display")
    country = serializers.CharField(source="get_country_display")
    region = serializers.CharField(source="get_region_display")
    # request_for_call = serializers.CharField(source="get_request_for_call_display")
    first_response_channel = serializers.CharField(source="get_first_response_channel_display")
    first_hpo_selection = serializers.CharField(source="get_first_hpo_selection_display")
    second_hpo_selection = serializers.CharField(source="get_second_hpo_selection_display")
    third_hpo_selection = serializers.CharField(source="get_third_hpo_selection_display")
    organisation_type = serializers.CharField(source="get_organisation_type_display")
    investment_type = serializers.CharField(source="get_investment_type_display")
    new_existing_investor = serializers.CharField(source="get_new_existing_investor_display")
    investor_involvement_level = serializers.CharField(source="get_investor_involvement_level_display")
    specific_investment_programme = serializers.CharField(source="get_specific_investment_programme_display")
    date_added_to_datahub = serializers.DateField(format="%d %B %Y")
    datahub_project_status = serializers.CharField(source="get_datahub_project_status_display")
    project_success_date = serializers.DateField(format="%d %B %Y")
    flag_status = serializers.SerializerMethodField()

    class Meta:
        model = models.Enquiry
        fields = "__all__"
        extra_fields = ['flag_status']
    
    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def get_flag_status(self, obj):
        flaggable_stages = [ref_data.EnquiryStage.AWAITING_RESPONSE, ref_data.EnquiryStage.ENGAGED]
        
        days_since_last_updated = (datetime.now() - obj.modified.replace(tzinfo=None)).days

        if obj.enquiry_stage in flaggable_stages:
            if days_since_last_updated > 28:
                return "flag-red"
            if days_since_last_updated > 14:
                return "flag-orange"
        return "no-flag"
