import pytest
from django.contrib.auth import SESSION_KEY
from django.test import Client
from django.urls import reverse
from rest_framework import status


from app.enquiries.models import (
    Enquirer,
    Enquiry,
    Owner,
)
from app.enquiries.tests.factories import (
    EnquirerFactory,
    EnquiryFactory,
    OwnerFactory,
)

RESET_URL = reverse('testfixtureapi:reset-fixtures')
SEED_USER_DATA = {
    'username': 'seeduser',
    'first_name': 'Seed',
    'last_name': 'User',
    'email': 'seed.user@example.com',
}


def test_url_not_found_if_not_setup(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = None
    response = Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_url_found_if_env_setup(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    response = Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_new_enquirer_removed_by_method(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    new_enquirer_pk = EnquirerFactory().pk
    Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    with pytest.raises(Enquirer.DoesNotExist):
        Enquirer.objects.get(pk=new_enquirer_pk)


@pytest.mark.django_db
def test_new_enquiry_removed_by_method(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    new_enquiry_pk = EnquiryFactory().pk
    Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    with pytest.raises(Enquiry.DoesNotExist):
        Enquiry.objects.get(pk=new_enquiry_pk)


@pytest.mark.django_db
def test_new_owner_removed_by_method(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    new_owner_pk = OwnerFactory().pk
    Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    with pytest.raises(Owner.DoesNotExist):
        Owner.objects.get(pk=new_owner_pk)


@pytest.mark.django_db
def test_fixture_owner_created_by_method(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    owner_email = 'ist.user.1@example.com'
    with pytest.raises(Owner.DoesNotExist):
        Owner.objects.get(email=owner_email)
    Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    assert Owner.objects.filter(email=owner_email).count() == 1


@pytest.mark.django_db
def test_fixture_enquirer_created_by_method(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    enquirer_email = 'evelyn.wang@example.com'
    with pytest.raises(Enquirer.DoesNotExist):
        Enquirer.objects.get(email=enquirer_email)
    Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    assert Enquirer.objects.filter(email=enquirer_email).count() == 1


@pytest.mark.django_db
def test_fixture_enquiry_created_by_method(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    enquiry_pk = 1
    with pytest.raises(Enquiry.DoesNotExist):
        Enquiry.objects.get(pk=enquiry_pk)
    Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    enquiry = Enquiry.objects.get(pk=enquiry_pk)
    assert enquiry.company_name == 'ABC Electronics Co.'


@pytest.mark.django_db
def test_seed_user_created_as_specified(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    Client().post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    created_user = Owner.objects.get(email=SEED_USER_DATA['email'])
    assert created_user.username == SEED_USER_DATA['username']
    assert created_user.first_name == SEED_USER_DATA['first_name']
    assert created_user.last_name == SEED_USER_DATA['last_name']


@pytest.mark.django_db
def test_seed_user_is_logged_in(settings):
    settings.ALLOW_TEST_FIXTURE_SETUP = True
    client = Client()
    assert SESSION_KEY not in client.session
    client.post(
        RESET_URL,
        SEED_USER_DATA,
        content_type='application/json'
    )
    assert SESSION_KEY in client.session
