import json

from babel.dates import format_date
from babel.numbers import format_number
from jingo import register

from affiliates.base.utils import absolutify as utils_absolutify, current_locale


@register.filter
def babel_date(date, format='long'):
    """
    Format a date properly for the current locale. Format can be one of
    'short', 'medium', 'long', or 'full'.
    """
    locale = current_locale()
    return format_date(date, format, locale)


@register.filter
def babel_number(number):
    """Format a number properly for the current locale."""
    locale = current_locale()
    return format_number(number, locale)


@register.function
def absolutify(*args, **kwargs):
    """Return the given url with an added domain and protocol."""
    return utils_absolutify(*args, **kwargs)


@register.filter
def jsonencode(data):
    return json.dumps(data)
