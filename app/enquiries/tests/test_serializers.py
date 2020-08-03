from django.test import TestCase

import app.enquiries.ref_data as ref_data
from app.enquiries import serializers
from app.enquiries.tests.factories import (
    EnquiryFactory,
    EnquirerFactory,
    OwnerFactory,
    get_display_value,
)


class EnquiriesSerializersTestCase(TestCase):
    def test_enquiry_serializer(self):
        """
        Test serialization of Enquiry object
        Ensures the format of date fields is as expected and choice field
        values match with their display value
        """
        enquiry = EnquiryFactory()
        sr_data = serializers.EnquiryDetailSerializer(enquiry).data
        self.assertEqual(enquiry.created.strftime("%d %B %Y"), sr_data["created"])
        self.assertEqual(enquiry.modified.strftime("%d %B %Y"), sr_data["modified"])
        self.assertEqual(
            enquiry.date_added_to_datahub.strftime("%d %B %Y"), sr_data["date_added_to_datahub"]
        )
        self.assertEqual(
            enquiry.project_success_date.strftime("%d %B %Y"), sr_data["project_success_date"]
        )
        self.assertEqual(
            get_display_value(ref_data.EnquiryStage, enquiry.enquiry_stage),
            sr_data["enquiry_stage"]
        )
        self.assertEqual(
            get_display_value(ref_data.InvestmentReadiness, enquiry.investment_readiness),
            sr_data["investment_readiness"]
        )
        self.assertEqual(
            get_display_value(
                ref_data.InvestmentProgramme, enquiry.specific_investment_programme,
            ),
            sr_data["specific_investment_programme"]
        )
        self.assertEqual(
            get_display_value(ref_data.Country, enquiry.country), sr_data["country"]
        )
        self.assertEqual(
            get_display_value(ref_data.PrimarySector, enquiry.primary_sector),
            sr_data["primary_sector"]
        )
        self.assertEqual(
            get_display_value(ref_data.InvestmentType, enquiry.investment_type),
            sr_data["investment_type"]
        )

    def test_enquirer_serializer(self):
        """
        Test serialization of Enquirer object ensure display values
        are as expected
        """
        enquirer = EnquirerFactory()
        sr_data = serializers.EnquirerDetailSerializer(enquirer).data
        self.assertEqual(enquirer.first_name, sr_data["first_name"])
        self.assertEqual(enquirer.last_name, sr_data["last_name"])
        self.assertEqual(enquirer.email, sr_data["email"])


class OwnerSerializerTestCase(TestCase):
    def test_owner_serializer(self):
        """
        Test serialization of Owner object ensure display values
        are as expected
        """
        owner = OwnerFactory()
        sr_data = serializers.OwnerSerializer(owner).data
        self.assertEqual(owner.first_name, sr_data["first_name"])
        self.assertEqual(owner.last_name, sr_data["last_name"])
        self.assertEqual(owner.email, sr_data["email"])
        self.assertEqual(owner.username, sr_data["username"])
