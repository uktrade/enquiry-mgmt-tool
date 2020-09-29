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
    @mock.patch('app.enquiries.common.adobe.AdobeClient.create_staging_profile')
    def test_process_latest_enquiries(self, mock_staging):
        mock_staging.return_value = {'PKey': 1}
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
    @mock.patch('app.enquiries.common.adobe.AdobeClient.start_workflow')
    @mock.patch('app.enquiries.common.adobe.AdobeClient.create_staging_profile')
    def test_process_workflow_kickoff(self, mock_staging, mock_wf):
        mock_staging.return_value = {'PKey': 1}
        mock_wf.return_value = {}
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
