# reviews/templatetags/reviews_extras.py

from django import template

register = template.Library()

@register.filter
def classname(value):
    return value.__class__.__name__
