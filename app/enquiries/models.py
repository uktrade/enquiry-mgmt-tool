import reversion

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

    first_name = models.CharField(max_length=MAX_LENGTH, verbose_name="First name")
    last_name = models.CharField(max_length=MAX_LENGTH, verbose_name="Last name")
    job_title = models.CharField(max_length=MAX_LENGTH, verbose_name="Job title")
    email = models.EmailField(
        max_length=MAX_LENGTH, blank=True, verbose_name="Email"
    )
    phone = models.CharField(max_length=MAX_LENGTH, verbose_name="Phone")
    email_consent = models.BooleanField(default=False, verbose_name="Email consent")
    phone_consent = models.BooleanField(default=False, verbose_name="Phone consent")
    request_for_call = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.RequestForCall.choices,
        default=ref_data.RequestForCall.DEFAULT,
        verbose_name="Call requested",
    )


class Owner(models.Model):
    """
    Model for the user assigned to an Enquiry
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


@reversion.register
class Enquiry(TimeStampedModel):
    """
    Model for investment Enquiry
    """

    company_name = models.CharField(
        max_length=MAX_LENGTH,
        help_text="Name of the company",
        verbose_name="Company name",
    )
    enquiry_stage = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.EnquiryStage.choices,
        default=ref_data.EnquiryStage.NEW,
        verbose_name="Enquiry stage",
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,
        related_name="owner",
        blank=True,
        null=True,
        help_text="User assigned to the enquiry",
        verbose_name="Owner",
    )
    enquiry_text = models.CharField(max_length=MAX_LENGTH, verbose_name="Enquiry text")
    investment_readiness = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentReadiness.choices,
        default=ref_data.InvestmentReadiness.DEFAULT,
        verbose_name="Investment readiness",
    )
    quality = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Quality.choices,
        default=ref_data.Quality.DEFAULT,
        verbose_name="Enquiry quality",
    )
    google_campaign = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Google campaign"
    )
    marketing_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.MarketingChannel.choices,
        default=ref_data.MarketingChannel.DEFAULT,
        verbose_name="Marketing channel",
    )
    how_they_heard_dit = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HowDidTheyHear.choices,
        default=ref_data.HowDidTheyHear.DEFAULT,
        verbose_name="How did they hear about DIT?",
    )
    website = models.URLField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Website"
    )
    primary_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.PrimarySector.choices,
        default=ref_data.PrimarySector.DEFAULT,
        verbose_name="Primary sector",
    )
    ist_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.IstSector.choices,
        default=ref_data.IstSector.DEFAULT,
        verbose_name="IST sector",
    )
    company_hq_address = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Company HQ address"
    )
    country = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Country.choices,
        default=ref_data.Country.DEFAULT,
        verbose_name="Country",
    )
    region = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Region.choices,
        default=ref_data.Region.DEFAULT,
        verbose_name="Region",
    )
    enquirer = models.ForeignKey(
        Enquirer,
        related_name="enquirer",
        on_delete=models.PROTECT,
        verbose_name="Enquirer",
    )
    first_response_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.FirstResponseChannel.choices,
        default=ref_data.FirstResponseChannel.DEFAULT,
        verbose_name="First response channel",
    )
    notes = models.TextField(verbose_name="Notes")
    first_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
        verbose_name="First HPO selection",
    )
    second_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
        verbose_name="Second HPO selection",
    )
    third_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
        verbose_name="Third HPO selection",
    )
    organisation_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.OrganisationType.choices,
        default=ref_data.OrganisationType.DEFAULT,
        verbose_name="Organisation type",
    )
    investment_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentType.choices,
        default=ref_data.InvestmentType.DEFAULT,
        verbose_name="Investment type",
    )
    project_name = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Project name"
    )
    project_description = models.TextField(
        blank=True, null=True, verbose_name="Project description"
    )
    anonymised_project_description = models.TextField(
        blank=True, null=True, verbose_name="Anonymised project description"
    )
    estimated_land_date = models.DateField(
        blank=True, null=True, verbose_name="Estimated land date"
    )
    new_existing_investor = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.NewExistingInvestor.choices,
        default=ref_data.NewExistingInvestor.DEFAULT,
        verbose_name="New or existing investor",
    )
    investor_involvement_level = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestorInvolvement.choices,
        default=ref_data.InvestorInvolvement.FDI_HUB_POST,
        verbose_name="Investor level of involvement",
    )
    specific_investment_programme = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentProgramme.choices,
        default=ref_data.InvestmentProgramme.IIGB,
        verbose_name="Specific investment programme",
    )
    crm = models.CharField(
        max_length=MAX_LENGTH,
        help_text="Name of the relationship manager",
        verbose_name="CRM",
    )
    project_code = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Project code"
    )
    date_added_to_datahub = models.DateField(
        blank=True, null=True, verbose_name="Date added to Data Hub"
    )
    datahub_project_status = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.DatahubProjectStatus.choices,
        default=ref_data.DatahubProjectStatus.DEFAULT,
        verbose_name="Data Hub project status",
    )
    project_success_date = models.DateField(
        blank=True, null=True, verbose_name="Project success date"
    )

    class Meta:
        ordering = ["created"]
