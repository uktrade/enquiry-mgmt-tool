from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def query_params_has_value(value, param_key, query_params):
    return str(value) in query_params.get_list(param_key)

@register.simple_tag
def query_params_value_selected(value, param_key, query_params, text='selected'):
    return f' {text}' if str(value) in query_params.getlist(param_key) else ''