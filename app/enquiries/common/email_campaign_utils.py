"""
This module handles the connection to Adobe Campaign, subscribing non responsinve leads
to an email campaign. The campaign prompts leads to fill in a 2nd qualification form,
requesting  call back.
The process includes a few steps:

Process 1:
1. collect enquiries which are marked as Non Responsive.
2. For each one, subscribe the lead to the adobe campaign.
3. Collect a log of each such subscription to ensure the next run picks up from the
   last subscription

    Example:
    ```
    from app.enquiries.common.email_campaign_utils import process_latest_enquiries
    process_latest_enquiries()

    ```

Process 2:
1. Collect any submission to the 2nd qualification form via activity stream.
2. Update Adobe Campaign that the lead has completed the 2nd qualification form.

    Example:
    ```
    process_second_qualifications()
    ```
Process 3:
1. Collect any leads marked as engaged. Unsubscribe them from the adobe campaign.

    Example:
    ```
    process_engaged_enquiry()
    ```
"""
import logging
from app.enquiries.models import Enquiry, EnquiryActionLog
import app.enquiries.ref_data as ref_data
from django.conf import settings
from django.utils import crypto, timezone
from .adobe import AdobeClient, AdobeCampaignRequestException
# from .as_utils import hawk_request


logger = logging.getLogger(__name__)

# The enquiry stage to use for triggering an unsubscribe
EXIT_STAGE = ref_data.EnquiryStage.SENT_TO_POST
ENQUIRY_SOURCE = 'EMT'


def process_latest_enquiries():
    """
    Get latest enquiries, created from the last fetch.
    """
    last_action_date = EnquiryActionLog.action_date_boundary(
        ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE)
    enquiries = Enquiry.objects.filter(
        enquiryactionlog__isnull=True,
        enquiry_stage__in=[ref_data.EnquiryStage.NON_RESPONSIVE],
    )
    if last_action_date:
        enquiries = enquiries.filter(created__gt=last_action_date)

    enquiries = enquiries.order_by('created')

    for enquiry in enquiries:
        process_enquiry(enquiry)
        logger.info(f'Processed enquiry {enquiry}')


def process_second_qualifications():
    """
    Collect second qualification submissions from the last time it was fetched
    successfuly.
    """
    last_action_date = EnquiryActionLog.objects.filter(
        action=ref_data.EnquiryAction.SECOND_QUALIFICATION_FORM
    ).order_by('-actioned_at').first()

    query = {
        "size": 50,
        "query": {
            "bool": {
                "filter": [
                    {"range": {"object.published": {"gte": last_action_date.actioned_at}}},
                    {
                        "term": {
                            settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY3:
                                settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE3
                        }
                    },
                    {
                        "term": {
                            settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_KEY2:
                                settings.ACTIVITY_STREAM_ENQUIRY_SEARCH_VALUE2
                        }
                    },
                    {
                        "bool": {
                            "must_not": {
                                "term": {
                                    "actor.dit:emailAddress": "noreply@invest.great.gov.uk"
                                }
                            }
                        }
                    },
                ]
            }
        },
        "sort": [{"published": "asc"}, {"id": "asc"}],
    }
    print(query)
    # for enquiry in enquiries:
    #     process_enquiry_update(enquiry)
    #     logger.info(f'Processed enquiry {enquiry}')


def process_engaged_enquiries():
    """
    Collect all enquiries marked with the `EXIT_STAGE` which will cause them
    to be unsubscribed from the campaign.
    """
    last_action_date = EnquiryActionLog.action_date_boundary(
        ref_data.EnquiryAction.MARKED_RESPONSIVE)

    enquiries = Enquiry.objects.filter(
        enquiryactionlog__isnull=True,
        enquiry_stage__in=[EXIT_STAGE],
    )
    if last_action_date:
        enquiries = enquiries.filter(created__gt=last_action_date)
    enquiries = enquiries.order_by(
        'created'
    )

    for enquiry in enquiries:
        process_engaged_enquiry(enquiry)
        logger.info(f'Processed engaged enquiry {enquiry}')


# def process_unsubscribes():
#     """
#     Process any unsubscribes made on the Adobe side, by clicking the unsubscribe link
#     on the email.
#     For each unsubscribe item :
#         - retrigger an activity stream event which will then reach consent service.
#         - update email consent on the specific enquiry
#     """
#     client = AdobeClient()
#     unsubscribers = client.get_unsubscribers()
#     for item in unsubscribers.get('content', []):
#         enquiry = Enquiry.objects.get(id=item.get('EMT_ID'))
#         enquirer = enquiry.enquirer
#         enquirer.email_consent = False
#         enquirer.save()
#         log = EnquiryActionLog.objects.create(
#             enquiry=enquiry,
#             action=ref_data.EnquiryAction.UNSUBSCRIBED_FROM_CAMPAIGN,
#             action_data=item,
#         )


def randword(size=8):
    return crypto.get_random_string(size)


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
    email = f'harel+{randword()}@harelmalka.com'
    client = AdobeClient()
    try:
        response = client.create_staging_profile(
            email=email,
            first_name=first_name,
            last_name=last_name,
            emt_id=emt_id,
            extra_data=additional_data
        )
        print(response)
        log = EnquiryActionLog.objects.create(
            enquiry=enquiry,
            action=ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE,
            action_data=response
        )
    except AdobeCampaignRequestException as exc:
        logger.exception('Error creating staging profiles in Adobe: %s', str(exc))
    finally:
        # kick off the workflow to process the updates
        client.start_workflow(settings.ADOBE_STAGING_WORKFLOW)
    return log


def process_enquiry_update(emt_id, phone=None, consent=None):
    """
    Create a staging record referencing an emt_id with an updated phone and consent,
    and new stage, to update the relevant profile.
    """
    log = None
    data = {
        'phone': phone,
        'phoneConsent': consent,
        'enquiry_stage': ref_data.EnquiryStage.NURTURE_AWAITING_RESPONSE,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    client = AdobeClient()
    try:
        response = client.create_staging_profile(
            emt_id=emt_id,
            extra_data=data,
        )
        log = log_action(
            action=ref_data.EnquiryAction.SECOND_QUALIFICATION_FORM,
            action_data=response,
            emt_id=emt_id
        )
    except AdobeCampaignRequestException as exc:
        logger.exception("Error updating enquiry stage in Adobe: %s", str(exc))
    finally:
        # kick off the workflow to process the updates
        client.start_workflow(settings.ADOBE_STAGING_WORKFLOW)
    return log


def process_engaged_enquiry(enquiry):
    """
    Update Adobe that a lead has now been marked as engaged and no
    longer required nurture. The lead will be unsubscribed from the campaign
    """
    additional_data = {
        'enquiry_stage': EXIT_STAGE,
        'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    client = AdobeClient()
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
    finally:
        # kick off the workflow to process the updates
        client.start_workflow(settings.ADOBE_STAGING_WORKFLOW)
    return log


def log_action(*, action, action_data, emt_id=None, enquiry=None):
    """
    Log an action for an enquiryt engagement with Adobe Campaign.
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
