from django.conf import settings
from django.forms import ModelForm

from app.enquiries.models import Enquiry, Enquirer


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
