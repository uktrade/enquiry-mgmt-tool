import pytz
import random
from datetime import datetime
from django.test import Client, TestCase
from django.urls import reverse
from django.http import QueryDict
from faker import Faker
from rest_framework import status

from app.enquiries.tests.factories import EnquiryFactory, get_random_item
from app.enquiries.models import Enquiry
from app.enquiries.views import filter_queryset
import app.enquiries.ref_data as ref_data


faker = Faker(["en_GB", "en_US", "ja_JP"])

FIXTURE_COUNT = 84

class EnquiryFiltersTestCase(TestCase):
    fixtures = ['84_enquiry-stages']
    def setUp(self):
        self.client = Client()
    def test_loaded_fixtures(self):
        num = Enquiry.objects.all().count()
        self.assertEqual(num, FIXTURE_COUNT)
    def test_filter_enquiry_stage_types(self):
        ENQUIRY_STAGES = [
            ref_data.EnquiryStage.NEW, ref_data.EnquiryStage.AWAITING_RESPONSE,
            ref_data.EnquiryStage.NON_FDI, ref_data.EnquiryStage.NON_RESPONSIVE,
            ref_data.EnquiryStage.POST_PROGRESSING, ref_data.EnquiryStage.SENT_TO_POST,
            ref_data.EnquiryStage.ADDED_TO_DATAHUB
        ]
        for STAGE in ENQUIRY_STAGES:
            query_str = f'enquiry_stage={STAGE}'
            print(query_str)
            qd = QueryDict(query_str)
            qs = Enquiry.objects.all()
            qs = filter_queryset(qs, qd)
            for e in qs.iterator():
                self.assertEqual(e.enquiry_stage == STAGE, True)
    def test_filter_enquiry_stages_none(self):
        qd = QueryDict()
        qs = Enquiry.objects.all()
        qs = filter_queryset(qs, qd)
        num = Enquiry.objects.all().count()
        self.assertEqual(num, FIXTURE_COUNT)

    def test_filter_multiple_values(self):
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
            self.assertEqual((e.enquiry_stage in allowed_stages) or (e.owner == user_keys[1]), True)

    def test_filter_bad_parameter_key(self):
        qd = QueryDict(f'bad_key1={ref_data.EnquiryStage.NON_FDI}&bad_key2={ref_data.EnquiryStage.POST_PROGRESSING}')
        qs = Enquiry.objects.all()
        qs = filter_queryset(qs, qd)
        num = Enquiry.objects.all().count()
        self.assertEqual(num, FIXTURE_COUNT)