import factory
import random

from faker import Faker

from app.enquiries.models import Enquirer, Enquiry
import app.enquiries.ref_data as ref_data

factory.Faker._DEFAULT_LOCALE = "en_GB"


def get_random_item(refdata_model):
    return random.choice(refdata_model.choices)[0]


class EnquirerFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    request_for_call = get_random_item(ref_data.RequestForCall)

    class Meta:
        model = Enquirer


class EnquiryFactory(factory.django.DjangoModelFactory):

    company_name = factory.Faker("company")
    enquiry_stage = get_random_item(ref_data.EnquiryStage)
    enquiry_text = factory.Faker("sentence")
    enquirer = factory.SubFactory(EnquirerFactory)
    investment_readiness = get_random_item(ref_data.InvestmentReadiness)
    quality = get_random_item(ref_data.Quality)
    marketing_channel = get_random_item(ref_data.MarketingChannel)
    how_they_heard_dit = get_random_item(ref_data.HowDidTheyHear)
    primary_sector = get_random_item(ref_data.PrimarySector)
    ist_sector = get_random_item(ref_data.IstSector)
    company_hq_address = factory.Faker("address")
    country = get_random_item(ref_data.Country)
    region = get_random_item(ref_data.Region)
    first_response_channel = get_random_item(ref_data.FirstResponseChannel)
    notes = factory.Faker("sentence", nb_words=20)
    first_hpo_selection = get_random_item(ref_data.HpoSelection)
    second_hpo_selection = get_random_item(ref_data.HpoSelection)
    third_hpo_selection = get_random_item(ref_data.HpoSelection)
    organisation_type = get_random_item(ref_data.OrganisationType)
    investment_type = get_random_item(ref_data.InvestmentType)
    project_name = factory.Faker("sentence", nb_words=4)
    project_description = factory.Faker("sentence", nb_words=10)
    anonymised_project_description = factory.Faker("sentence", nb_words=10)
    new_existing_investor = get_random_item(ref_data.NewExistingInvestor)
    investor_involvement_level = get_random_item(ref_data.InvestorInvolvement)
    specific_investment_programme = get_random_item(ref_data.InvestmentProgramme)
    datahub_project_status = get_random_item(ref_data.DatahubProjectStatus)
    crm = factory.Faker("first_name")

    class Meta:
        model = Enquiry
