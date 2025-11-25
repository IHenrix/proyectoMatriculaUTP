"""
Custom template tags and filters
"""
from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def get(dictionary, key):
    """
    Template filter to get a value from a dictionary.

    Usage: {{ dict|get:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def mul(value, arg):
    """
    Multiply the value by the argument.

    Usage: {{ value|mul:arg }}
    """
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return None


@register.filter
def div(value, arg):
    """
    Divide the value by the argument.

    Usage: {{ value|div:arg }}
    """
    try:
        return Decimal(str(value)) / Decimal(str(arg))
    except (ValueError, TypeError, ZeroDivisionError):
        return None
