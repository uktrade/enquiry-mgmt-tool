from django.conf import settings
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory

import app.enquiries.ref_data as ref_data
from app.enquiries.models import Enquiry, Enquirer

MAX_LENGTH = settings.CHAR_FIELD_MAX_LENGTH


class EnquiryForm(ModelForm):
    """
    Enquiry edit form

    It is based on Enquiry model, the additional fields defined are for Enquirer.
    We have a single view to edit both Enquiry and Enquirer details hence they
    are included in this form. The primary key of Enquirer is received in the
    form data which is used to update these fields.
    """

    first_name = forms.CharField(max_length=MAX_LENGTH, label="First name")
    last_name = forms.CharField(max_length=MAX_LENGTH, label="Last name")
    job_title = forms.CharField(max_length=MAX_LENGTH, label="Job title")
    email = forms.EmailField(max_length=MAX_LENGTH, label="Email")
    phone = forms.CharField(max_length=MAX_LENGTH, label="Phone")
    email_consent = forms.BooleanField(required=False, initial=False, label="Email consent")
    phone_consent = forms.BooleanField(required=False, initial=False, label="Phone consent")
    request_for_call = forms.ChoiceField(
        choices=ref_data.RequestForCall.choices,
        initial=ref_data.RequestForCall.DEFAULT,
        label="Call requested",
    )

    class Meta:
        model = Enquiry
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        enquirer = self.instance.enquirer
        self.fields['first_name'].initial = enquirer.first_name
        self.fields['last_name'].initial = enquirer.last_name
        self.fields['job_title'].initial = enquirer.job_title
        self.fields['email'].initial = enquirer.email
        self.fields['phone'].initial = enquirer.phone
        self.fields['email_consent'].initial = enquirer.email_consent
        self.fields['phone_consent'].initial = enquirer.phone_consent
        self.fields['request_for_call'].initial = enquirer.request_for_call

    def save(self, commit=True):
        enquiry = super().save(commit=False)
        enquirer = self.cleaned_data["enquirer"]
        enquirer.first_name = self.cleaned_data['first_name']
        enquirer.last_name = self.cleaned_data['last_name']
        enquirer.job_title = self.cleaned_data['job_title']
        enquirer.email = self.cleaned_data['email']
        enquirer.phone = self.cleaned_data['phone']
        enquirer.email_consent = self.cleaned_data['email_consent']
        enquirer.phone_consent = self.cleaned_data['phone_consent']
        enquirer.request_for_call = self.cleaned_data['request_for_call']
        enquirer.save()

        if commit:
            enquiry.save()

        return enquiry
