from babel.dates import format_date
from bleach import clean
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
    return format_date(date, format)


@register.filter
def bleach(str, *args, **kwargs):
    return Markup(clean(str, *args, **kwargs))
