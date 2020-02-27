import pytz
import random
from datetime import datetime
from django.test import Client, TestCase
from django.urls import reverse
from django.http import QueryDict
from faker import Faker
from rest_framework import status

from app.enquiries.tests.factories import EnquiryFactory, get_random_item
from app.enquiries.models import Enquiry, Enquirer, Owner
from app.enquiries.views import filter_queryset
from app.enquiries.tests.test_views import canned_enquiry
import app.enquiries.ref_data as ref_data


faker = Faker(["en_GB", "en_US", "ja_JP"])

EXISTING_RECORDS = 20

def apply_filter(key, value) -> QueryDict:
    query_str = f'{key}={value}'
    print(query_str)
    qd = QueryDict(query_str)
    qs = Enquiry.objects.all()
    return filter_queryset(qs, qd)

def populate_db():
    num_enquirers = 3
    # enquirer
    Enquirer.objects.bulk_create([
        Enquirer(
            first_name= "Evelyn",
            last_name= "Wang",
            job_title= "Director",
            email= "evelyn.wang@example.com",
            phone= "+86 88 8888 8888",
            email_consent= True,
            phone_consent= True,
            request_for_call= "YES_OTHER"
        ),
        Enquirer(
            first_name= "Jeff",
            last_name= "Bezo",
            job_title= "Editor",
            email= "jeff.bezos@washingtonpost.com",
            phone= "+1 202 334 6000",
            email_consent= True,
            phone_consent= False,
            request_for_call= "YES_AFTERNOON"
        ),
        Enquirer(
            first_name= "Nanny",
            last_name= "Maroon",
            job_title= "Founder",
            email= "nanny.maroon@bluemountain.jm",
            phone= "+876 000 176",
            email_consent= False,
            phone_consent= False,
            request_for_call= "NO"  
        )
    ])
    for en in Enquirer.objects.all().iterator():
        print(en.pk)
        print(en.id)
    # enquiries
    for i in range(EXISTING_RECORDS):
        enquirer_id = i + 1 if i < num_enquirers else (i % num_enquirers) + 1
        print('enquirer id:', enquirer_id)
        params = canned_enquiry()
        e = Enquiry(**params)
        e.enquirer = Enquirer.objects.get(pk = enquirer_id)
        print(e)

FIXTURE_COUNT = 84

class EnquiryFiltersTestCase(TestCase):
    fixtures = ['enquiries']
    def setUp(self):
        # populate_db()
        self.client = Client()
    def test_loaded_fixtures(self):
        num = Enquiry.objects.all().count()
        self.assertEqual(num, FIXTURE_COUNT)
    
    def test_filter_company_name(self):
        existing_name = 'Alphabet Projects'
        existing_name_partial = existing_name[:-8]
        non_existing_name = 'chinese industries'
        existing_records = 12

        # exact match
        qs = apply_filter('company_name', existing_name)
        self.assertEqual(qs.count(), existing_records)
        # partial match
        qs = apply_filter('company_name', existing_name_partial)
        self.assertEqual(qs.count(), existing_records)
        # no match
        qs = apply_filter('company_name', non_existing_name)
        self.assertEqual(qs.count(), 0, 'should return no matches')

    def test_filter_email(self):
        enquirer = Enquirer.objects.first()
        # exact match
        qs = apply_filter('enquirer_email', enquirer.email)
        self.assertTrue(qs.count() > 1, f'enquirer email should match some enquiries')
        # partial string (no match)
        qs = apply_filter('enquirer_email', enquirer.email[:-2])
        self.assertEqual(qs.count(), 0 , f'enquirer email should match no enquiries')

    def test_filter_enquiry_stage_types(self):

        for STAGE, label in ref_data.EnquiryStage.choices:
            qs = apply_filter('enquiry_stage', STAGE)
            qs_count = qs.count()
            self.assertGreater(qs_count, 0, f'queryset for {STAGE} should be greater than 0')
            for e in qs.iterator():
                self.assertEqual(e.enquiry_stage, STAGE, f'enquiry_stage should equal {STAGE}')
    
    def test_filter_owner(self):
        owners = Owner.objects.all()
        print('owners count', owners.count())
        for owner in owners.iterator():
            qs = apply_filter('owner', owner.user.id)
            print(qs)
            qs_count = qs.count()
            self.assertGreater(qs_count, 0, f'query for {owner} should be greater than 0')
            for e in qs.iterator():
                self.assertEqual(e.owner, owner, f'owner should equal {owner}')

    def test_filter_enquiry_stages_none(self):
        qd = QueryDict()
        qs = Enquiry.objects.all()
        qs = filter_queryset(qs, qd)
        num = Enquiry.objects.all().count()
        self.assertEqual(num, FIXTURE_COUNT)

    def test_filter_enquiry_stages_multiple_values(self):
        '''Filter won't be applied'''
        allowed_stages = [ref_data.EnquiryStage.NON_FDI, ref_data.EnquiryStage.POST_PROGRESSING]
        qd = QueryDict(f'enquiry_stage={ref_data.EnquiryStage.NON_FDI}&enquiry_stage={ref_data.EnquiryStage.POST_PROGRESSING}')
        qs = Enquiry.objects.all()
        qs = filter_queryset(qs, qd)
        for e in qs.iterator():
            self.assertEqual(e.enquiry_stage in allowed_stages, True)

    def test_filter_multiple_keys(self):
        '''Filter won't be applied'''
        allowed_stages = [ref_data.EnquiryStage.NON_FDI, ref_data.EnquiryStage.POST_PROGRESSING]
        user_keys = [3, 5]
        qd = QueryDict(f'enquiry_stage={ref_data.EnquiryStage.NON_FDI}&owner__user__id={user_keys[1]}')
        qs = Enquiry.objects.all()
        qs = filter_queryset(qs, qd)
        for e in qs.iterator():
            print(e.enquiry_stage)
            self.assertEqual((e.enquiry_stage in allowed_stages) or (e.owner == user_keys[1]), True)

    def test_date_received_before(self):
        date_before_none = '2017-01-09'
        date_before_one = '2017-01-10'
        # search should return none
        qs = apply_filter('date_created_before', date_before_none)
        self.assertEqual(qs.count(), 0, f'should return no records before {date_before_none}')
        # search should return one
        qs = apply_filter('date_created_before', date_before_one)
        self.assertEqual(qs.count(), 1, f'should return 1 records before {date_before_one}')

    def test_date_received_after(self):
        # @TODO fixed boundary error
        date_after_none = '2020-02-13'
        date_after_one = '2020-02-10'
        # search should return none
        qs = apply_filter('date_created_after', date_after_none)
        self.assertEqual(qs.count(), 0, f'should return no records before {date_after_none}')
        # search should return one
        qs = apply_filter('date_created_after', date_after_one)
        self.assertEqual(qs.count(), 1, f'should return 1 records before {date_after_one}')

    def test_filter_bad_parameter_key(self):
        qd = QueryDict(f'bad_key1={ref_data.EnquiryStage.NON_FDI}&bad_key2={ref_data.EnquiryStage.POST_PROGRESSING}')
        qs = Enquiry.objects.all()
        qs = filter_queryset(qs, qd)
        num = Enquiry.objects.all().count()
        self.assertEqual(num, FIXTURE_COUNT, f'should not perform and filtering and retun the full queryset')