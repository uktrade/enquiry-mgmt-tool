import datetime
import app.enquiries.ref_data as ref_data
from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from faker import Faker
from freezegun import freeze_time
from unittest import mock
from app.enquiries.models import Enquiry, Enquirer, EnquiryActionLog
from app.enquiries.common import email_campaign_utils as campaign
from app.enquiries.common.adobe import AdobeClient


faker = Faker()


class TestAdobeCampaign(TestCase):
    @freeze_time()
    def setUp(self):
        self.enquirer = Enquirer.objects.create(
            first_name=faker.name(),
            last_name=faker.name(),
            email=faker.email(),
            job_title='Manager',
            phone_country_code='1',
            phone=faker.phone_number(),
            email_consent=True,
            phone_consent=True,
            request_for_call=ref_data.RequestForCall.YES_AFTERNOON.value,
        )
        self.enquiry = Enquiry.objects.create(
            enquirer=self.enquirer,
            company_name=faker.company(),
            company_hq_address=faker.address(),
            date_received=datetime.datetime.now(),
            enquiry_stage=ref_data.EnquiryStage.NON_RESPONSIVE.value,
            how_they_heard_dit=ref_data.HowDidTheyHear.INTERNET_SEARCH.value,
            ist_sector=ref_data.ISTSector.AEM.value,
            primary_sector=ref_data.PrimarySector.AEROSPACE.value,
            website='http://example.com',
        )
        self.enquiry_done = Enquiry.objects.create(
            enquirer=self.enquirer,
            company_name=faker.company(),
            company_hq_address=faker.address(),
            date_received=datetime.datetime.now(),
            enquiry_stage=ref_data.EnquiryStage.SENT_TO_POST.value,
            how_they_heard_dit=ref_data.HowDidTheyHear.INTERNET_SEARCH.value,
            ist_sector=ref_data.ISTSector.AEM.value,
            primary_sector=ref_data.PrimarySector.AEROSPACE.value,
            website='http://example.com',
        )
        self.additional_data = {
            'companyName': self.enquiry.company_name,
            'companyHQAddress': self.enquiry.company_hq_address,
            'country': self.enquiry.country,
            'emailConsent': self.enquiry.enquirer.email_consent,
            'enquiry_stage': self.enquiry.enquiry_stage,
            'howTheyHeard_DIT': self.enquiry.how_they_heard_dit,
            'istSector': self.enquiry.ist_sector,
            'jobTitle': self.enquiry.enquirer.job_title,
            'phone': self.enquiry.enquirer.phone,
            'phoneConsent': self.enquiry.enquirer.phone_consent,
            'primarySector': self.enquiry.primary_sector,
            'requestForCall': self.enquiry.enquirer.request_for_call,
            'website': self.enquiry.website,
            'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'enquiryDate': self.enquiry.created.strftime('%Y-%m-%d %H:%M:%S'),
            'ditSource': campaign.ENQUIRY_SOURCE,
        }

    @freeze_time()
    @mock.patch('app.enquiries.common.adobe.AdobeClient.get_token')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.create_staging_profile')
    def test_process_latest_enquiries(self, mock_staging, mock_token):
        mock_staging.return_value = {'PKey': 1}
        mock_token.return_value = 'token'
        campaign.process_latest_enquiries()
        client = AdobeClient()
        client.create_staging_profile.assert_called_with(
            email=self.enquirer.email,
            first_name=self.enquirer.first_name,
            last_name=self.enquirer.last_name,
            emt_id=self.enquiry.id,
            extra_data=self.additional_data
        )

    @freeze_time()
    @mock.patch('app.enquiries.common.adobe.AdobeClient.get_token')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.start_workflow')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.create_staging_profile')
    def test_process_workflow_kickoff(self, mock_staging, mock_wf, mock_token):
        mock_staging.return_value = {'PKey': 1}
        mock_wf.return_value = {}
        mock_token.return_value = 'token'
        campaign.process_latest_enquiries()
        client = AdobeClient()
        client.create_staging_profile.assert_called_with(
            email=self.enquirer.email,
            first_name=self.enquirer.first_name,
            last_name=self.enquirer.last_name,
            emt_id=self.enquiry.id,
            extra_data=self.additional_data
        )
        client.start_workflow.assert_called_with(settings.ADOBE_STAGING_WORKFLOW)

    @freeze_time()
    @mock.patch('app.enquiries.common.adobe.AdobeClient.get_token')
    @mock.patch('app.enquiries.common.as_utils.hawk_request')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.start_workflow')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.create_staging_profile')
    def test_process_second_qualification(self, mock_staging, mock_wf, mock_as, mock_token):
        mock_staging.return_value = {'PKey': 1}
        mock_wf.return_value = {}
        mock_token.return_value = 'token'
        mock_as.return_value.ok = True
        mock_as.return_value.json.return_value = {
            'hits': {
                'hits': [
                    {
                        '_source': {
                            'object': {
                                settings.ACTIVITY_STREAM_ENQUIRY_DATA_OBJ: {
                                    'data': {
                                        'emt_id': self.enquiry.id,
                                        'phone_number': '0771231234',
                                        'arrange_callback': 'yes',
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
        campaign.process_second_qualifications()
        client = AdobeClient()
        client.create_staging_profile.assert_called_once_with(
            emt_id=self.enquiry.id,
            extra_data={
                'phone': '0771231234',
                'phoneConsent': True,
                'enquiry_stage': ref_data.EnquiryStage.NURTURE_AWAITING_RESPONSE,
                'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        )
        client.start_workflow.assert_called_with(settings.ADOBE_STAGING_WORKFLOW)

    @freeze_time()
    @mock.patch('app.enquiries.common.adobe.AdobeClient.get_token')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.start_workflow')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.create_staging_profile')
    def test_process_engaged(self, mock_staging, mock_wf, mock_token):
        mock_staging.return_value = {'PKey': 2}
        mock_wf.return_value = {}
        mock_token.return_value = 'token'
        EnquiryActionLog.objects.create(
            enquiry=self.enquiry_done,
            action=ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE,
        )
        campaign.process_engaged_enquiries()
        client = AdobeClient()
        client.create_staging_profile.assert_called_once_with(
            emt_id=self.enquiry_done.id,
            extra_data={
                'enquiry_stage': campaign.EXIT_STAGE.value,
                'uploadDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        )
        client.start_workflow.assert_called_with(settings.ADOBE_STAGING_WORKFLOW)

    @freeze_time()
    def test_log_action(self):
        action = ref_data.EnquiryAction.EMAIL_CAMPAIGN_SUBSCRIBE
        campaign.log_action(
            action=action,
            enquiry=self.enquiry,
            emt_id=self.enquiry.id,
            action_data={'PKey': 1}
        )

        last_action_date = EnquiryActionLog.get_last_action_date(action)
        self.assertEqual(last_action_date.enquiry.id, self.enquiry.id)
