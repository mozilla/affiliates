import locale

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.translation import get_language

from babel.core import Locale, UnknownLocaleError
from funfactory.urlresolvers import reverse
from product_details import product_details


def absolutify(url, https=False, cdn=False):
    """
    Return the given url with an added domain and protocol.

    Use https=True for https, cdn=True to use settings.CDN_DOMAIN as
    the domain.
    """
    protocol = 'http://' if not https else 'https://'
    if cdn and settings.CDN_DOMAIN:
        domain = settings.CDN_DOMAIN
    else:
        domain = Site.objects.get_current().domain

    return ''.join((protocol, domain, url))


def unicode_choice_sorted(choices):
    """
    Sorts a list of 2-tuples by the second value, using a unicode-safe sort.
    """
    return sorted(choices, cmp=lambda x, y: locale.strcoll(x[1], y[1]))

def country_choices():
    """Return a localized, sorted list of tuples of country names and values."""
    items = product_details.get_regions(get_language()).items()
    items.append(('', '---'))  # Empty choice
    return unicode_choice_sorted(items)


def redirect(to, permanent=False, **kwargs):
    """
    Returns a redirect response by applying funfactory's locale-aware reverse
    to the given string.

    Pass in permanent=True to return a permanent redirect. All other keyword
    arguments are passed to reverse.
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    return redirect_class(reverse(to, **kwargs))


def current_locale():
    """
    Return the current Locale object (from Babel). Defaults to en-US if locale
    does not exist.
    """
    try:
        return Locale.parse(get_language(), sep='-')
    except UnknownLocaleError:
        # Default to en-US
        return Locale('en', 'US')
