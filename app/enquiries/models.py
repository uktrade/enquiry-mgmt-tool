from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

import app.enquiries.ref_data as ref_data

MAX_LENGTH = settings.CHAR_FIELD_MAX_LENGTH


class Enquirer(models.Model):
    """
    Model for Enquirer details
    """
    first_name = models.CharField(max_length=MAX_LENGTH)
    last_name = models.CharField(max_length=MAX_LENGTH)
    job_title = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField(unique=True, max_length=MAX_LENGTH, blank=True)
    phone = models.CharField(max_length=MAX_LENGTH)
    email_consent = models.BooleanField(default=False)
    phone_consent = models.BooleanField(default=False)
    request_for_call = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.RequestForCall.choices,
        default=ref_data.RequestForCall.DEFAULT,
    )


class Owner(models.Model):
    """
    Model for the user assigned to an Enquiry
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Enquiry(TimeStampedModel):
    """
    Model for investment Enquiry
    """
    owner = models.ForeignKey(
        Owner, on_delete=models.PROTECT, related_name="owner", blank=True, null=True
    )
    company_name = models.CharField(max_length=MAX_LENGTH, help_text="Name of the company")
    enquiry_stage = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.EnquiryStage.choices,
        default=ref_data.EnquiryStage.NEW,
    )
    owner = models.ForeignKey(
        Owner, on_delete=models.PROTECT, related_name="owner", blank=True, null=True, help_text="User assigned to the enquiry"
    )
    enquiry_text = models.CharField(max_length=MAX_LENGTH)
    investment_readiness = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentReadiness.choices,
        default=ref_data.InvestmentReadiness.DEFAULT,
    )
    quality = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Quality.choices,
        default=ref_data.Quality.DEFAULT,
    )
    google_campaign = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    marketing_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.MarketingChannel.choices,
        default=ref_data.MarketingChannel.DEFAULT,
    )
    how_they_heard_dit = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HowDidTheyHear.choices,
        default=ref_data.HowDidTheyHear.DEFAULT,
    )
    website = models.URLField(max_length=MAX_LENGTH, blank=True, null=True)
    primary_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.PrimarySector.choices,
        default=ref_data.PrimarySector.DEFAULT,
    )
    ist_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.IstSector.choices,
        default=ref_data.IstSector.DEFAULT,
    )
    company_hq_address = models.CharField(max_length=MAX_LENGTH)
    country = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Country.choices,
        default=ref_data.Country.DEFAULT,
    )
    region = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Region.choices,
        default=ref_data.Region.DEFAULT,
    )
    enquirer = models.ForeignKey(Enquirer, related_name="enquirer", on_delete=models.PROTECT)
    first_response_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.FirstResponseChannel.choices,
        default=ref_data.FirstResponseChannel.DEFAULT,
    )
    notes = models.TextField()
    first_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
    )
    second_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
    )
    third_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
    )
    organisation_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.OrganisationType.choices,
        default=ref_data.OrganisationType.DEFAULT,
    )
    investment_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentType.choices,
        default=ref_data.InvestmentType.DEFAULT,
    )
    project_name = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    anonymised_project_description = models.TextField(blank=True, null=True)
    estimated_land_date = models.DateField(blank=True, null=True)
    new_existing_investor = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.NewExistingInvestor.choices,
        default=ref_data.NewExistingInvestor.DEFAULT,
    )
    investor_involvement_level = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestorInvolvement.choices,
        default=ref_data.InvestorInvolvement.FDI_HUB_POST,
    )
    specific_investment_programme = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentProgramme.choices,
        default=ref_data.InvestmentProgramme.IIGB,
    )
    crm = models.CharField(max_length=MAX_LENGTH, help_text="Name of the relationship manager")
    project_code = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    date_added_to_datahub = models.DateField(blank=True, null=True)
    datahub_project_status = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.DatahubProjectStatus.choices,
        default=ref_data.DatahubProjectStatus.DEFAULT,
    )
    project_success_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["created"]

