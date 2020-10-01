"""
This module handles the connection to Adobe Campaign, subscribing non responsive leads
to an email campaign. The campaign prompts enquirers to fill in a 2nd qualification form,
requesting  call back.
The process includes a few steps:

Process 1:
1. collect enquiries which are marked as Non Responsive.
2. For each one, subscribe the enquirers to the adobe campaign.
3. Collect a log of each such subscription to ensure the next run picks up from the
   last subscription

    Example:
    ```
    from app.enquiries.common.email_campaign_utils import process_latest_enquiries
    process_latest_enquiries()

    ```

Process 2:
1. Collect any submission to the 2nd qualification form via activity stream.
2. Update Adobe Campaign that the enquirer has completed the 2nd qualification form.

    Example:
    ```
    process_second_qualifications()
    ```
Process 3:
1. Collect any enquiries marked as sent to post. Unsubscribe them from the adobe campaign.

    Example:
    ```
    process_engaged_enquiry()
    ```
"""
import logging
from app.enquiries.models import Enquiry, EnquiryActionLog
import app.enquiries.ref_data as ref_data
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .adobe import AdobeClient, AdobeCampaignRequestException
from .as_utils import get_new_second_qualification_forms


logger = logging.getLogger(__name__)

# The enquiry stage to use for triggering an unsubscribe
EXIT_STAGE = ref_data.EnquiryStage.SENT_TO_POST
# The enquiry stagee to set after second qualification form is submitted
SECOND_QUALIFICATION_STAGE = ref_data.EnquiryStage.NURTURE_AWAITING_RESPONSE
ENQUIRY_SOURCE = 'EMT'


def process_latest_enquiries():
    """
    Get latest enquiries, created from the last fetch.
    """
    last_action_date = EnquiryActionLog.get_last_action_date(
        ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE)
    enquiries = Enquiry.objects.filter(
        enquiryactionlog__isnull=True,
        enquiry_stage__in=[ref_data.EnquiryStage.NON_RESPONSIVE],
    )
    if last_action_date:
        enquiries = enquiries.filter(created__gt=last_action_date.actioned_at)

    enquiries = enquiries.order_by('created')
    total_enquiries = enquiries.count()
    if total_enquiries > 0:
        logger.info('Processing %s enquiries', total_enquiries)
        for enquiry in enquiries:
            process_enquiry(enquiry)
            logger.info('Processed enquiry %s', enquiry)

        # kick off the workflow to process the updates
        start_staging_workflow()


def process_second_qualifications():
    """
    Collect second qualification submissions from the last time it was fetched
    successfuly.
    """
    last_action_date = EnquiryActionLog.objects.filter(
        action=ref_data.EnquiryAction.SECOND_QUALIFICATION_FORM
    ).order_by('-actioned_at').first()
    submissions = get_new_second_qualification_forms(
        last_datetime=last_action_date.actioned_at if last_action_date else None
    )
    for submission in submissions:
        data = submission["_source"]["object"][settings.ACTIVITY_STREAM_ENQUIRY_DATA_OBJ]["data"]
        process_enquiry_update(
            emt_id=data.get('emt_id'),
            phone=data.get('phone_number'),
            consent=data.get('arrange_callback') == 'yes'
        )
    # kick off the workflow to process the updates
    start_staging_workflow()


def process_engaged_enquiries():
    """
    Collect all enquiries marked with the `EXIT_STAGE` which will cause them
    to be unsubscribed from the campaign.
    """
    last_action_date = EnquiryActionLog.get_last_action_date(
        ref_data.EnquiryAction.MARKED_RESPONSIVE)

    enquiries = Enquiry.objects.filter(
        enquiryactionlog__isnull=True,
        enquiry_stage__in=[EXIT_STAGE],
    )
    if last_action_date:
        enquiries = enquiries.filter(created__gt=last_action_date.actioned_at)
    enquiries = enquiries.order_by(
        'created'
    )

    for enquiry in enquiries:
        process_engaged_enquiry(enquiry)
        logger.info('Processed engaged enquiry %s', enquiry)

    # kick off the workflow to process the updates
    start_staging_workflow()


def process_enquiry(enquiry):
    enquirer = enquiry.enquirer
    email = enquirer.email
    first_name = enquirer.first_name
    last_name = enquirer.last_name
    emt_id = enquiry.id
    additional_data = {
        'companyName': enquiry.company_name,
        'companyHQAddress': enquiry.company_hq_address,
        'country': enquiry.country,
        'emailConsent': enquiry.enquirer.email_consent,
        'enquiry_stage': enquiry.enquiry_stage,
        'howTheyHeard_DIT': enquiry.how_they_heard_dit,
        'istSector': enquiry.ist_sector,
        'jobTitle': enquiry.enquirer.job_title,
        'phone': enquiry.enquirer.phone,
        'phoneConsent': enquiry.enquirer.phone_consent,
        'primarySector': enquiry.primary_sector,
        'requestForCall': enquiry.enquirer.request_for_call,
        'website': enquiry.website,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'enquiryDate': enquiry.created.strftime('%Y-%m-%d %H:%M:%S'),
        'ditSource': ENQUIRY_SOURCE,
    }
    logger.info("Processing enquiry. Email=%s", email)
    client = AdobeClient()
    log = None
    try:
        response = client.create_staging_profile(
            email=email,
            first_name=first_name,
            last_name=last_name,
            emt_id=emt_id,
            extra_data=additional_data
        )
        log = EnquiryActionLog.objects.create(
            enquiry=enquiry,
            action=ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE,
            action_data=response
        )
    except AdobeCampaignRequestException as exc:
        logger.exception('Error creating staging profiles in Adobe: %s', str(exc))
    return log


@transaction.atomic
def process_enquiry_update(emt_id, phone=None, consent=None):
    """
    Updates the enquiry record with the new stage and create a staging
    record referencing an emt_id with an updated phone and consent,
    and new stage, to update the relevant profile.
    """
    log = None
    data = {
        'phone': phone,
        'phoneConsent': consent,
        'enquiry_stage': SECOND_QUALIFICATION_STAGE,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    client = AdobeClient()
    try:
        enquiry = Enquiry.objects.get(id=emt_id)
        enquiry.enquiry_stage = SECOND_QUALIFICATION_STAGE
        enquiry.save()
        enquirer = enquiry.enquirer
        if phone and phone != enquirer.phone:
            enquirer.phone = phone
            enquirer.save()
        response = client.create_staging_profile(
            emt_id=emt_id,
            extra_data=data,
        )
        log = log_action(
            action=ref_data.EnquiryAction.SECOND_QUALIFICATION_FORM,
            action_data=response,
            emt_id=emt_id
        )
    except Enquiry.DoesNotExist:
        logger.exception(
            "Enquiry %s does not exist. Cannot update stage for second qualification.", emt_id)
    except AdobeCampaignRequestException as exc:
        logger.exception("Error updating enquiry stage in Adobe: %s", str(exc))
    return log


def process_engaged_enquiry(enquiry):
    """
    Update Adobe that a lead has now been marked as engaged and no
    longer requires nurturing. The lead will be unsubscribed from the campaign
    """
    additional_data = {
        'enquiry_stage': EXIT_STAGE.value,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    client = AdobeClient()
    log = None
    try:
        response = client.create_staging_profile(
            emt_id=enquiry.id,
            extra_data=additional_data
        )
        log = log_action(
            action=ref_data.EnquiryAction.UNSUBSCRIBED_FROM_CAMPAIGN,
            action_data=response,
            enquiry=enquiry
        )
    except AdobeCampaignRequestException as exc:
        logger.exception("Error updating engaged enquiry in Adobe: %s", str(exc))
    return log


def start_staging_workflow():
    """
    Initiate the Adobe workflow to process the staging area
    """
    client = AdobeClient()
    return client.start_workflow(settings.ADOBE_STAGING_WORKFLOW)


def log_action(*, action, action_data, emt_id=None, enquiry=None):
    """
    Log an action for an enquiry engagement with Adobe Campaign.
    """
    log = None
    try:
        enquiry = Enquiry.objects.get(id=emt_id) if not enquiry and emt_id else enquiry
        log = EnquiryActionLog.objects.create(
            enquiry=enquiry,
            action=action,
            action_data=action_data,
        )
    except Enquiry.DoesNotExist:
        logger.error('Second qualification process error: Invalid enquiry id: %s', emt_id)
    return log
