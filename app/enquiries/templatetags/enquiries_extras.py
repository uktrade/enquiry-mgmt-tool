from django import template

from app.enquiries import models
from app.enquiries import serializers

register = template.Library()


@register.filter
def get_field_verbose_name(instance, field_name):
    fields = instance._meta.fields

    target = list(filter(lambda f: f.name == field_name, fields))
    if not target:
        return "Unknown field"

    target = target[0]
    if target.verbose_name:
        return target.verbose_name
    else:
        return target.name


@register.filter
def get_field_value(instance, field_name):

    if isinstance(instance, models.Enquiry):
        serializer = serializers.EnquiryDetailSerializer(instance)
    elif isinstance(instance, models.Enquirer):
        serializer = serializers.EnquirerDetailSerializer(instance)
    elif isinstance(instance, models.Owner):
        serializer = serializers.OwnerSerializer(instance)

    return serializer.data[field_name]
