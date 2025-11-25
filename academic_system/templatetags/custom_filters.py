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


@register.filter
def format_decimal(value):
    """
    Formatea un número decimal con punto (no coma) y 2 decimales.
    Ej: 15.50 en lugar de 15,50

    Usage: {{ value|format_decimal }}
    """
    if value is None:
        return ''
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return value
