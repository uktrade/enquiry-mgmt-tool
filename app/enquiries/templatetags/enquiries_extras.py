from django import template

from app.enquiries import models
from app.enquiries import serializers

register = template.Library()

field_error_msgs = {
    "company_name": "Company name cannot be left blank",
    "company_hq_address": "Company address cannot be left blank",
    "enquiry_text": "Enquiry text cannot be left blank",
    "website": "Enter a valid website eg http://www.example.com",
    "first_name": "Enquirer first name is required",
    "last_name": "Enquirer last name is required",
    "job_title": "Enquirer job title is required",
    "email": "Enquirer email is required",
    "phone": "Enquirer phone is required",
}

@register.filter
def enquiry_field_error_msg(field):
    return field_error_msgs.get(field)


def get_instance_field(instance, field_name):
    fields = instance._meta.fields
    target = list(filter(lambda f: f.name == field_name, fields))
    return target[0]

@register.filter
def get_field_verbose_name(instance, field_name):
    field = get_instance_field(instance, field_name)
    if field.verbose_name:
        return field.verbose_name
    else:
        return field.name


@register.filter
def get_field_value(instance, field_name):

    if isinstance(instance, models.Enquiry):
        serializer = serializers.EnquiryDetailSerializer(instance)
    elif isinstance(instance, models.Enquirer):
        serializer = serializers.EnquirerDetailSerializer(instance)
    elif isinstance(instance, models.Owner):
        serializer = serializers.OwnerSerializer(instance)

    return serializer.data[field_name]


@register.filter
def get_field_choices(instance, field_name):
    field = get_instance_field(instance, field_name)
    return field.choices


@register.filter
def get_attribute(instance, field_name):
    field = get_instance_field(instance, field_name)
    return field.value_from_object(instance)


@register.filter
def get_owners(instance):
    return [owner for owner in models.Owner.objects.all()]


@register.filter
def get_date(instance, field_name):
    field = get_instance_field(instance, field_name)

    if field.value_from_object(instance):
        return field.value_from_object(instance).strftime('%Y-%m-%d')
    else:
        return None

@register.filter
def query_params_has_value(value, param_key, query_params):
    return str(value) in query_params.get_list(param_key)

@register.simple_tag
def query_params_value_selected(value, param_key, query_params, text='selected'):
    return f' {text}' if str(value) in query_params.getlist(param_key) else ''
