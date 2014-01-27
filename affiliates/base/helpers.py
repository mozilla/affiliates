from babel.dates import format_date
from babel.numbers import format_number
from jingo import register

from affiliates.shared.utils import current_locale


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
