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
from app.enquiries.views import filtered_queryset
from app.enquiries.tests.test_views import canned_enquiry
import app.enquiries.ref_data as ref_data


faker = Faker(["en_GB", "en_US", "ja_JP"])

EXISTING_RECORDS = 20


def apply_filter(key, value) -> QueryDict:
    query_str = f"{key}={value}"
    print(query_str)
    qd = QueryDict(query_str)
    qs = Enquiry.objects.all()
    return filtered_queryset(qs, qd)


COMPANY_NAMES = ['Alphabet Projects', 'MARS EXPORTS (UAE)', '1Company', 'Testing Company Ltd', 'MATCHBOX LTD', 'ABC Electronics Co.', 'Venus Ltd']
COMPANY_NAMES_LEN = len(COMPANY_NAMES)
EMAIL_ADDRESSES = ['user1@live.com', 'user2@live.com', 'user3@live.com', 'user4@live.com', 'user5@live.com',]
EMAIL_ADDRESSES_LEN = len(EMAIL_ADDRESSES)
FIXTURE_COUNT = 84


class EnquiryFiltersTestCase(TestCase):
    # fixtures = ["enquiries"]

    def setUp(self):
        # populate_db()
        self.client = Client()
        self.enquiries = [EnquiryFactory() for i in range(20)]
        self.enquiry_counts = {
            'stage': {},
            'company_name': {},
            'enquirer_email': {},
            'owner': {},
        }
        self.enquiry_company_name_counts = {}
        OWNERS = list(Owner.objects.all())
        OWNERS_LEN = len(OWNERS)
        for i, enquiry in enumerate(self.enquiries):
            company_name_index = i if i < COMPANY_NAMES_LEN else i % COMPANY_NAMES_LEN
            company_name = COMPANY_NAMES[ company_name_index ]
            stage = random.choice(ref_data.EnquiryStage.choices)[0]
            email_index = i if i < EMAIL_ADDRESSES_LEN else i % EMAIL_ADDRESSES_LEN
            email_address = EMAIL_ADDRESSES[email_index]
            owner_index = i if i < OWNERS_LEN else i % OWNERS_LEN
            owner = OWNERS[owner_index]
            # set values
            enquiry.enquiry_stage = stage
            enquiry.company_name = company_name
            enquiry.email_address = email_address
            enquiry.owner = owner

            enquiry.save()
            # increment stage counts
            if stage in self.enquiry_counts['stage']:
                self.enquiry_counts['stage'][stage] += 1
            else:
                self.enquiry_counts['stage'][stage] = 1
            # increment company name counts
            if company_name in self.enquiry_counts['company_name']:
                self.enquiry_counts['company_name'][company_name] += 1
            else:
                self.enquiry_counts['company_name'][company_name] = 1
            # increment enquiry_email counts
            if company_name in self.enquiry_counts['enquirer_email']:
                self.enquiry_counts['enquirer_email'][email_address] += 1
            else:
                self.enquiry_counts['enquirer_email'][email_address] = 1
            
            if owner.id in self.enquiry_counts['owner']:
                self.enquiry_counts['owner'][owner.id] += 1
            else:
                self.enquiry_counts['owner'][owner.id] = 1

        # print(self.enquiry_counts)
        # print(Owner.objects.all().count())

    def test_filter_enquiry_stage(self):
        random_enquiry = random.choice(self.enquiries)
        queryset = apply_filter("enquiry_stage", random_enquiry.enquiry_stage)
        self.assertEqual(
            self.enquiry_counts['stage'][random_enquiry.enquiry_stage],
            len(queryset),
            f"Filtering stage: {random_enquiry.enquiry_stage}, should match enquiry count: {self.enquiry_counts['stage'][random_enquiry.enquiry_stage]}"
            )

    def test_filter_company_name(self):
        random_enquiry = random.choice(self.enquiries)
        queryset = apply_filter("company_name", random_enquiry.company_name)
        self.assertEqual(
            self.enquiry_counts['company_name'][random_enquiry.company_name],
            len(queryset),
            f"Filtering company_name: {random_enquiry.company_name}, should match enquiry count: {self.enquiry_counts['company_name'][random_enquiry.company_name]}"
            )

    def test_filter_owner(self):
        random_enquiry = random.choice(self.enquiries)
        owner_id = random_enquiry.owner.id
        queryset = apply_filter("owner", owner_id)
        self.assertEqual(
            self.enquiry_counts['owner'][owner_id],
            len(queryset),
            f"Filtering owner: {random_enquiry.owner}, should match enquiry count: {self.enquiry_counts['owner'][owner_id]}"
            )
