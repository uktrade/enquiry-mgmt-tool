from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

import app.enquiries.ref_data as ref_data

MAX_LENGTH = settings.CHAR_FIELD_MAX_LENGTH


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Enquiry(TimeStampedModel):
    owner = models.ForeignKey(
        Owner, on_delete=models.PROTECT, related_name="owner", blank=True, null=True
    )
    company_name = models.CharField(max_length=MAX_LENGTH)
    enquiry_stage = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.EnquiryStage.CHOICES,
        default=ref_data.EnquiryStage.NEW,
    )
    enquiry_text = models.CharField(max_length=MAX_LENGTH)
    investment_readiness = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentReadiness.CHOICES,
        default=ref_data.InvestmentReadiness.DEFAULT,
    )
    quality = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Quality.CHOICES,
        default=ref_data.Quality.DEFAULT,
    )
    google_campaign = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    marketing_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.MarketingChannel.CHOICES,
        default=ref_data.MarketingChannel.DEFAULT,
    )
    how_they_heard_dit = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HowDidTheyHear.CHOICES,
        default=ref_data.HowDidTheyHear.DEFAULT,
    )
    website = models.URLField(max_length=MAX_LENGTH, blank=True, null=True)
    primary_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.PrimarySector.CHOICES,
        default=ref_data.PrimarySector.DEFAULT,
    )
    ist_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.IstSector.CHOICES,
        default=ref_data.IstSector.DEFAULT,
    )
    company_hq_address = models.CharField(max_length=MAX_LENGTH)
    country = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Country.CHOICES,
        default=ref_data.Country.DEFAULT,
    )
    region = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Region.CHOICES,
        default=ref_data.Region.DEFAULT,
    )
    enquirer_first_name = models.CharField(max_length=MAX_LENGTH)
    enquirer_last_name = models.CharField(max_length=MAX_LENGTH)
    job_title = models.CharField(max_length=MAX_LENGTH)
    enquirer_email = models.EmailField(max_length=MAX_LENGTH, blank=True)
    enquirer_phone = models.CharField(max_length=MAX_LENGTH)
    email_consent = models.BooleanField(default=False)
    phone_consent = models.BooleanField(default=False)
    request_for_call = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.RequestForCall.CHOICES,
        default=ref_data.RequestForCall.DEFAULT,
    )
    first_response_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.FirstResponseChannel.CHOICES,
        default=ref_data.FirstResponseChannel.DEFAULT,
    )
    notes = models.TextField()
    first_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.CHOICES,
        default=ref_data.HpoSelection.DEFAULT,
    )
    second_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.CHOICES,
        default=ref_data.HpoSelection.DEFAULT,
    )
    third_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.CHOICES,
        default=ref_data.HpoSelection.DEFAULT,
    )
    organisation_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.OrganisationType.CHOICES,
        default=ref_data.OrganisationType.DEFAULT,
    )
    investment_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentType.CHOICES,
        default=ref_data.InvestmentType.DEFAULT,
    )
    project_name = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    anonymised_project_description = models.TextField(blank=True, null=True)
    estimated_land_date = models.DateField(blank=True, null=True)
    new_existing_investor = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.NewExistingInvestor.CHOICES,
        default=ref_data.NewExistingInvestor.DEFAULT,
    )
    investor_involvement_level = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestorInvolvement.CHOICES,
        default=ref_data.InvestorInvolvement.FDI_HUB_POST,
    )
    specific_investment_programme = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentProgramme.CHOICES,
        default=ref_data.InvestmentProgramme.IIGB,
    )
    crm = models.CharField(max_length=MAX_LENGTH)
    project_code = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    date_added_to_datahub = models.DateTimeField(blank=True, null=True)
    datahub_project_status = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.DatahubProjectStatus.CHOICES,
        default=ref_data.DatahubProjectStatus.DEFAULT,
    )
    project_success_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["created"]

    def save(self, *args, **kwargs):
        # Validate whether the selected value is a valid choice
        choice_fields = [field for field in self._meta.get_fields() if field.choices]
        for index, field in enumerate(choice_fields):
            choice = field.value_from_object(self)
            # if the value is blank, use default choice
            if not choice:
                choice = field.default
            if not any(choice in _tuple for _tuple in field.choices):
                raise ValueError(
                    f"Invalid choice {choice} provided for the field {field.name}"
                )
        super().save(*args, **kwargs)
