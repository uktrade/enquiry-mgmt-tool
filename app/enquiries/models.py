from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField

import app.enquiries.ref_data as ref_data

MAX_LENGTH = settings.CHAR_FIELD_MAX_LENGTH


class Enquirer(models.Model):
    """
    Model for Enquirer details
    """

    first_name = models.CharField(max_length=MAX_LENGTH, blank=True, verbose_name="First name")
    last_name = models.CharField(max_length=MAX_LENGTH, verbose_name="Last name")
    job_title = models.CharField(max_length=MAX_LENGTH, verbose_name="Job title")
    email = models.TextField(blank=True, verbose_name="Email")
    phone_country_code = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="Telephone country code"
    )
    phone = models.CharField(max_length=MAX_LENGTH, blank=True, verbose_name="Phone")
    request_for_call = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.RequestForCall.choices,
        default=ref_data.RequestForCall.DEFAULT,
        verbose_name="Call requested",
    )


class Owner(AbstractUser):
    """
    Customer user model used by the app.
    Each :class:`Enquiry` has an :class:`Owner`.
    """

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"


class Enquiry(TimeStampedModel):
    """
    Model for investment Enquiry

    Includes an optional :attr:`date_received` field to allow a differentiation
    between when the `enquiry` is uploaded to the system and when it was
    received by our teams.
    """

    #: Company name
    company_name = models.CharField(
        max_length=MAX_LENGTH, help_text="Name of the company", blank=True,
        verbose_name="Company name"
    )
    #: Date the enquiry was received
    date_received = models.DateTimeField(
        blank=True,
        null=True,
    )
    #: Stage of the enquiry, one of :attr:`ref_data.EnquiryStage.choices`
    enquiry_stage = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.EnquiryStage.choices,
        default=ref_data.EnquiryStage.NEW,
        verbose_name="Enquiry stage",
    )
    #: The :class:`Owner` of the enquiry
    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,
        related_name="owner",
        blank=True,
        null=True,
        help_text="User assigned to the enquiry",
        verbose_name="Owner",
    )
    #: Enquiry text
    enquiry_text = models.TextField(verbose_name="Enquiry text", editable=False,)
    #: Stage of the enquiry, one of :attr:`ref_data.InvestmentReadiness.choices`
    investment_readiness = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentReadiness.choices,
        default=ref_data.InvestmentReadiness.DEFAULT,
        blank=True,
        verbose_name="Investment readiness",
    )
    #: Stage of the enquiry, one of :attr:`ref_data.Quality.choices`
    quality = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Quality.choices,
        default=ref_data.Quality.DEFAULT,
        verbose_name="Enquiry quality",
    )
    #: Id of the related Google campaign
    google_campaign = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Google campaign"
    )
    #: Stage of the enquiry, one of :attr:`ref_data.MarketingChannel.choices`
    marketing_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.MarketingChannel.choices,
        default=ref_data.MarketingChannel.DEFAULT,
        verbose_name="Marketing channel",
    )
    #: How did the enquirer hear about DIT
    how_they_heard_dit = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HowDidTheyHear.choices,
        default=ref_data.HowDidTheyHear.DEFAULT,
        verbose_name="How did they hear about DIT?",
    )
    #: Website URL
    website = models.TextField(blank=True, verbose_name="Website")
    #: Stage of the enquiry, one of :attr:`ref_data.PrimarySector.choices`
    primary_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.PrimarySector.choices,
        default=ref_data.PrimarySector.DEFAULT,
        verbose_name="Primary sector",
    )
    #: The IST sector, one of :attr:`ref_data.ISTSector.choices`
    ist_sector = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.ISTSector.choices,
        default=ref_data.ISTSector.DEFAULT,
        verbose_name="IST sector",
    )
    #: Company headquarter address
    company_hq_address = models.CharField(max_length=MAX_LENGTH, verbose_name="Company HQ address")
    #: The IST sector, one of :attr:`ref_data.Country.choices`
    country = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Country.choices,
        default=ref_data.Country.DEFAULT,
        verbose_name="Country",
    )
    #: The IST sector, one of :attr:`ref_data.Region.choices`
    region = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.Region.choices,
        default=ref_data.Region.DEFAULT,
        verbose_name="Region",
    )
    #: The :class:`Enquirer`
    enquirer = models.ForeignKey(
        Enquirer, related_name="enquirer", on_delete=models.PROTECT, verbose_name="Enquirer",
    )
    #: The IST sector, one of :attr:`ref_data.FirstResponseChannel.choices`
    first_response_channel = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.FirstResponseChannel.choices,
        default=ref_data.FirstResponseChannel.DEFAULT,
        verbose_name="First response channel",
    )
    #: Extra notes
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    #: First HPO selection, one of :attr:`ref_data.HpoSelection.choices`
    first_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
        verbose_name="First HPO selection",
    )
    #: Second HPO selection, one of :attr:`ref_data.HpoSelection.choices`
    second_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
        verbose_name="Second HPO selection",
    )
    #: Third HPO selection, one of :attr:`ref_data.HpoSelection.choices`
    third_hpo_selection = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.HpoSelection.choices,
        default=ref_data.HpoSelection.DEFAULT,
        verbose_name="Third HPO selection",
    )
    #: Third HPO selection, one of :attr:`ref_data.OrganisationType.choices`
    organisation_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.OrganisationType.choices,
        default=ref_data.OrganisationType.DEFAULT,
        verbose_name="Organisation type",
    )
    #: Third HPO selection, one of :attr:`ref_data.InvestmentType.choices`
    investment_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentType.choices,
        default=ref_data.InvestmentType.DEFAULT,
        verbose_name="Investment type",
    )
    #: Project name
    project_name = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Project name"
    )
    #: Project description
    project_description = models.TextField(
        blank=True, null=True, verbose_name="Project description"
    )
    #: Anonymised project description
    anonymised_project_description = models.TextField(
        blank=True, null=True, verbose_name="Anonymised project description"
    )
    #: Estimated land date
    estimated_land_date = models.DateField(
        blank=True, null=True, verbose_name="Estimated land date"
    )
    #: Third HPO selection, one of :attr:`ref_data.NewExistingInvestor.choices`
    new_existing_investor = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.NewExistingInvestor.choices,
        default=ref_data.NewExistingInvestor.DEFAULT,
        verbose_name="New or existing investor",
    )
    #: Third HPO selection, one of :attr:`ref_data.InvestorInvolvement.choices`
    investor_involvement_level = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestorInvolvement.choices,
        default=ref_data.InvestorInvolvement.FDI_HUB_POST,
        verbose_name="Investor level of involvement",
    )
    #: Third HPO selection, one of :attr:`ref_data.InvestmentProgramme.choices`
    specific_investment_programme = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.InvestmentProgramme.choices,
        default=ref_data.InvestmentProgramme.IIGB,
        verbose_name="Specific investment programme",
    )
    #: Client relationship manager
    client_relationship_manager = models.CharField(
        max_length=MAX_LENGTH,
        help_text="Name of the client relationship manager",
        blank=True,
        null=True,
        verbose_name="Client Relationship Manager",
    )
    #: Project code
    project_code = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Project code"
    )
    #: Date added to DataHub
    date_added_to_datahub = models.DateField(
        blank=True, null=True, verbose_name="Date added to Data Hub"
    )
    #: DataHub project status
    datahub_project_status = models.CharField(
        max_length=MAX_LENGTH,
        choices=ref_data.DatahubProjectStatus.choices,
        default=ref_data.DatahubProjectStatus.DEFAULT,
        verbose_name="Data Hub project status",
    )
    #: Project success date
    project_success_date = models.DateField(
        blank=True, null=True, verbose_name="Project success date"
    )

    # If the Enquiry for the company that already exists in DH then user can assign
    # that company details to below fields when editing an Enquiry
    dh_company_id = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Company id in Data Hub",
    )
    dh_company_number = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Company number in Data Hub",
    )
    dh_duns_number = models.CharField(
        max_length=MAX_LENGTH, blank=True, null=True, verbose_name="Duns number",
    )
    dh_assigned_company_name = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Company in Data Hub",
        help_text="Name of the company in Data Hub",
    )
    dh_company_address = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name="Company address in Data Hub",
        help_text="Address of the company in Data Hub",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Enquiries"


class ReceivedEnquiryCursor(models.Model):
    """
    New enquiries data is pulled from |activity-stream|_ at regular intervals.
    This model tracks the timestamp and object id of the last item received.
    They are used to fetch the next set of results.
    """

    index = models.CharField(
        max_length=MAX_LENGTH, help_text="Index of the object", blank=True, null=True,
    )
    object_id = models.CharField(
        max_length=MAX_LENGTH,
        help_text="Id of the last object in the results returned by AS corresponding to the index",
        blank=True,
        null=True,
    )


class FailedEnquiry(models.Model):
    """
    Model to track failed enquiries when processing the data from |activity-stream|_
    """

    index = models.CharField(
        max_length=MAX_LENGTH, help_text="Index of the object", blank=True, null=True,
    )
    object_id = models.CharField(
        max_length=MAX_LENGTH, help_text="Id of the failed object", blank=True, null=True,
    )
    html_body = models.TextField(blank=True, null=True, verbose_name="HTML body")
    text_body = models.TextField(blank=True, null=True, verbose_name="Text body")


class EnquiryActionLog(models.Model):
    enquiry = models.ForeignKey(Enquiry, null=False, blank=False, on_delete=models.PROTECT)
    action = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        choices=ref_data.EnquiryAction.choices,
        default=ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE)
    actioned_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    action_data = JSONField(default=dict)

    def __str__(self):
        return f"{self.action}: {self.enquiry}"

    @staticmethod
    def get_last_action_date(action):
        """
        Return the last EnquiryActionLog for a specified action type.
        This record will contain the last time that action was performed.
        Returns None if no such action was done before.
        """
        return EnquiryActionLog.objects.filter(
            action=action
        ).order_by('-actioned_at').first()
