from django.utils.translation import get_language

import bleach
from babel.core import Locale
from babel.dates import format_date
from babel.numbers import format_number
from jingo import register
from jinja2 import Markup


@register.filter
def wizard_active(step, current):
    """
    Return the proper classname for the step div in the badge wizard.

    The current step needs a 'selected' class while the following step needs a
    'next-selected' class to color the tip of the arrow properly.
    """
    if current == step:
        return 'selected'
    elif (current + 1) == step:
        return 'next-selected'


@register.filter
def babel_date(date, format='long'):
    """
    Format a date properly for the current locale. Format can be one of
    'short', 'medium', 'long', or 'full'.
    """
    locale = Locale.parse(get_language(), sep='-')
    return format_date(date, format, locale)


@register.filter
def clean(str, *args, **kwargs):
    return Markup(bleach.clean(str, *args, **kwargs))


@register.filter
def linkify(str, *args, **kwargs):
    return Markup(bleach.linkify(str, *args, **kwargs))


@register.filter
def babel_number(number):
    """Format a number properly for the current locale."""
    locale = Locale.parse(get_language(), sep='-')
    return format_number(number, locale)
