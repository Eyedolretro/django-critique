# reviews/templatetags/custom_tags.py

from django import template

register = template.Library()

@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)




 

