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
import datetime
import logging

import pytz
from django.conf import settings
from django.db import transaction
from django.utils import timezone

import app.enquiries.ref_data as ref_data
from app.enquiries.common import consent
from app.enquiries.models import Enquiry, EnquiryActionLog
from .adobe import AdobeClient, AdobeCampaignRequestException
from .as_utils import get_new_second_qualification_forms

logger = logging.getLogger(__name__)

# The enquiry stage to use for triggering an unsubscribe
EXIT_STAGE = ref_data.EnquiryStage.SENT_TO_POST
# The enquiry stagee to set after second qualification form is submitted
SECOND_QUALIFICATION_STAGE = ref_data.EnquiryStage.NURTURE_AWAITING_RESPONSE
ENQUIRY_SOURCE = 'EMT'
# These error codes mean a retry is not possible (email invalid for example)
TERMINAL_ERROR_CODES = [
    'XTK-170049'
]


def process_latest_enquiries():
    """
    Get latest enquiries, which were not yet processed.
    """
    enquiries = Enquiry.objects.filter(
        enquiryactionlog__isnull=True,
        enquiry_stage__in=[
            ref_data.EnquiryStage.NON_RESPONSIVE
        ],
    )
    if settings.NON_RESPONSIVE_ENQUIRY_INITIAL_LOAD_DATE:
        last_action_date = datetime.datetime.strptime(
            settings.NON_RESPONSIVE_ENQUIRY_INITIAL_LOAD_DATE,
            "%d-%B-%Y"
        )
        last_action_date = pytz.UTC.localize(last_action_date)
        enquiries = enquiries.filter(date_received__gt=last_action_date)
    enquiries = enquiries.order_by('date_received')
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
    successfully.
    """
    last_action = EnquiryActionLog.get_last_action_date(
        ref_data.EnquiryAction.SECOND_QUALIFICATION_FORM
    )
    submissions = get_new_second_qualification_forms(
        last_datetime=last_action.actioned_at.date() if last_action else None
    )
    for submission in submissions:
        data = submission["_source"]["object"][settings.ACTIVITY_STREAM_ENQUIRY_DATA_OBJ]

        emt_id = data.get('emt_id')
        if not emt_id:
            logger.warning("Emt_id not provided for second qualification form")
            continue

        try:
            process_enquiry_update(
                emt_id=emt_id,
                phone=data.get('phone_number'),
                consent=data.get('arrange_callback') == 'yes'
            )
        except Exception as e:
            logger.exception(e)

    # kick off the workflow to process the updates
    start_staging_workflow()


def process_engaged_enquiries():
    """
    Collect all enquiries marked with the `EXIT_STAGE` which will cause them
    to be unsubscribed from the campaign.
    """
    # get enquiries that have been subscribed before and are now
    # in the exit stage
    enquiries = Enquiry.objects.filter(
        enquiryactionlog__action=ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE,
        enquiry_stage__in=[EXIT_STAGE],
    ).exclude(
        enquiryactionlog__action=ref_data.EnquiryAction.UNSUBSCRIBED_FROM_CAMPAIGN
    )
    enquiries = enquiries.order_by(
        'date_received'
    )

    for enquiry in enquiries:
        try:
            process_engaged_enquiry(enquiry)
        except Exception as e:
            logger.exception(e)
        logger.info('Processed engaged enquiry %s', enquiry)

    # kick off the workflow to process the updates
    start_staging_workflow()


def process_enquiry(enquiry):
    enquirer = enquiry.enquirer
    email = enquirer.email
    emt_id = enquiry.id
    data = serialize_enquiry(enquiry)
    logger.info("Processing enquiry. Email=%s", email)
    client = AdobeClient()
    log = None
    try:
        response = client.create_staging_profile(data=data)
        log = EnquiryActionLog.objects.create(
            enquiry=enquiry,
            action=ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE,
            action_data=response
        )
    except AdobeCampaignRequestException as exc:
        logger.exception('Error creating staging profiles in Adobe: %s', str(exc))
        # if the failure is known and there is no need to retry, log it.
        if any([code in exc.message for code in TERMINAL_ERROR_CODES]):
            logger.warning("Enquiry %s failed and will not be retried: [email=%s]", emt_id, email)
            log = EnquiryActionLog.objects.create(
                enquiry=enquiry,
                action=ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE,
                action_data={
                    "error": exc.message
                }
            )
    return log


@transaction.atomic
def process_enquiry_update(emt_id, phone=None, consent=None):
    """
    Updates the enquiry record with the new stage and create a staging
    record referencing an emt_id with an updated phone and consent,
    and new stage, to update the relevant profile.
    """
    data = {
        'phone': phone,
        'phoneConsent': consent,
        'enquiry_stage': SECOND_QUALIFICATION_STAGE,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    client = AdobeClient()
    try:
        enquiry = Enquiry.objects.get(id=emt_id)
        # check if this has already been processed
        has_processed = EnquiryActionLog.objects.filter(
            enquiry=enquiry,
            action=ref_data.EnquiryAction.SECOND_QUALIFICATION_FORM
        ).exists()
        if has_processed:
            return
        enquiry.enquiry_stage = SECOND_QUALIFICATION_STAGE
        enquiry.save()
        enquirer = enquiry.enquirer
        if phone and phone != enquirer.phone:
            enquirer.phone = phone
            enquirer.save()
        enquiry.refresh_from_db()
        response = client.create_staging_profile(
            data=serialize_enquiry(enquiry, **data),
        )
        log_action(
            action=ref_data.EnquiryAction.SECOND_QUALIFICATION_FORM,
            action_data=response,
            emt_id=emt_id
        )
    except Enquiry.DoesNotExist:
        logger.exception(
            "Enquiry %s does not exist. Cannot update stage for second qualification.", emt_id)
    except AdobeCampaignRequestException as exc:
        logger.exception("Error updating enquiry stage in Adobe: %s", str(exc))
    return


def process_engaged_enquiry(enquiry):
    """
    Update Adobe that a lead has now been marked as engaged and no
    longer requires nurturing. The lead will be unsubscribed from the campaign
    """
    data = {
        'enquiry_stage': EXIT_STAGE.value,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    client = AdobeClient()
    log = None
    try:
        response = client.create_staging_profile(
            data=serialize_enquiry(enquiry, **data)
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


def serialize_enquiry(enquiry, **kwargs):
    """
    Serialize an enquiry for Adobe, and overlay any additional kwargs on top
    overwriting any fields if present.
    """
    serialized = {
        'emt_id': enquiry.id,
        'email': enquiry.enquirer.email,
        'firstName': enquiry.enquirer.first_name,
        'lastName': enquiry.enquirer.last_name,
        'companyName': enquiry.company_name,
        'companyHQAddress': enquiry.company_hq_address,
        'country': enquiry.country,
        'emailConsent': consent.check_consent(key=enquiry.enquirer.email),
        'enquiry_stage': enquiry.enquiry_stage,
        'howTheyHeard_DIT': enquiry.how_they_heard_dit,
        'istSector': enquiry.ist_sector,
        'jobTitle': enquiry.enquirer.job_title,
        'phone': enquiry.enquirer.phone,
        'phoneConsent': consent.check_consent(key=enquiry.enquirer.phone),
        'primarySector': enquiry.primary_sector,
        'requestForCall': enquiry.enquirer.request_for_call,
        'website': enquiry.website,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'enquiryDate': enquiry.date_received.strftime('%Y-%m-%d %H:%M:%S'),
        'ditSource': ENQUIRY_SOURCE,
    }
    serialized.update(kwargs)
    return serialized
