from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from app.enquiries import models

class EnquirerSerializer(serializers.ModelSerializer):
    request_for_call = serializers.CharField(source="get_request_for_call_display")

    class Meta:
        model = models.Enquirer
        fields = "__all__"

class OwnerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Owner
        fields = "__all__"

    def get_user(self, obj):
        return obj


class EnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Enquiry
        fields = "__all__"


class EnquiryDetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    enquirer = EnquirerSerializer()
    created = serializers.DateTimeField(format="%d %b %Y")
    modified = serializers.DateTimeField(format="%d %b %Y")
    enquiry_stage = serializers.CharField(source="get_enquiry_stage_display")
    investment_readiness = serializers.CharField(source="get_investment_readiness_display")
    quality = serializers.CharField(source="get_quality_display")
    marketing_channel = serializers.CharField(source="get_marketing_channel_display")
    how_they_heard_dit = serializers.CharField(source="get_how_they_heard_dit_display")
    primary_sector = serializers.CharField(source="get_primary_sector_display")
    ist_sector = serializers.CharField(source="get_ist_sector_display")
    country = serializers.CharField(source="get_country_display")
    region = serializers.CharField(source="get_region_display")
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

    class Meta:
        model = models.Enquiry
        fields = "__all__"
