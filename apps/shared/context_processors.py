from django.conf import settings
from django.utils.translation import get_language

from babel.dates import get_month_names

from shared.utils import current_locale


def common(request):
    """Adds commonly-needed settings across the site."""
    return {'FACEBOOK_APP_URL': settings.FACEBOOK_APP_URL}


def l10n(request):
    """Adds language information to template contexts."""
    locale = get_language()
    ctx = {'LOCALE': locale}
    if locale and locale in settings.LANGUAGES:
        ctx['LANGUAGE'] = settings.LANGUAGES[locale]
    return ctx


def month_year_picker(request):
    """Adds localized date info for the month-year picker widget."""
    locale = current_locale()

    return {
        'mypicker_months_short': get_month_names('abbreviated', locale=locale),
        'mypicker_months_long': get_month_names('wide', locale=locale)
    }
