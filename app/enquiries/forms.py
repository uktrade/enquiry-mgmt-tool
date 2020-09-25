from dal import autocomplete
from django.forms import ModelForm, ChoiceField
from django.urls import reverse_lazy

from app.enquiries.models import Enquiry, Enquirer


class EnquirerForm(ModelForm):
    """:class:`app.enquiries.models.Enquirer` edit form """

    class Meta:
        model = Enquirer
        fields = "__all__"


class AutocompleteField(ChoiceField):
    widget = autocomplete.Select2(url=reverse_lazy("dh-adviser-search"))

    # We need to disable deep copying, otherwise setting the choices dynamically
    # won't take effect.
    def __deepcopy__(self, *args, **kwargs):
        return self


class EnquiryForm(ModelForm):
    """:class:`app.enquiries.models.Enquiry` edit form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The only reason we are overriding the constructor is that the
        # autocomplete field is validated against the field's choices, which
        # can only be hardcoded on the field's instantiation. Not only we don't
        # need this validation, which is preventing the form submission, but
        # surprisingly if the initial (previously saved) value is not one of the
        # choices, the field will not be prepopulated with it.
        # The workaround is to add both the initial and the new value as valid
        # choices dynamically.
        client_relationship_manager_initial = self.initial.get("client_relationship_manager")
        client_relationship_manager_data = self.data.get("client_relationship_manager")

        self.fields["client_relationship_manager"].choices = (
            (client_relationship_manager_data, client_relationship_manager_data),
            (client_relationship_manager_initial, client_relationship_manager_initial),
        )

    client_relationship_manager = AutocompleteField(required=False)

    class Meta:
        model = Enquiry
        exclude = ('datahub_project_status', 'date_received')
