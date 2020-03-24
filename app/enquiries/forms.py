from django.db import transaction
from django.conf import settings
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory

import app.enquiries.ref_data as ref_data
from app.enquiries.models import Enquiry, Enquirer

MAX_LENGTH = settings.CHAR_FIELD_MAX_LENGTH


class EnquirerForm(ModelForm):
    """ Enquirer edit form """

    class Meta:
        model = Enquirer
        fields = "__all__"


class EnquiryForm(ModelForm):
    """ Enquiry edit form """

    class Meta:
        model = Enquiry
        fields = "__all__"
