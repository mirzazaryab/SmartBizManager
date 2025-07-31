from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    return dictionary.get(str(key), 0)

@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0