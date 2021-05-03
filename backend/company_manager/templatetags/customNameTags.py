from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def custom_name_tag(value, arg):
    """ Create a custom Name Tag in the template"""
    return "button-{}-id_{}".format(arg,value)
