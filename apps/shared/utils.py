from locale import strcoll as locale_strcoll
from urlparse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.functional import lazy
from django.utils.translation import get_language

import tower
from babel.core import Locale, UnknownLocaleError
from funfactory.urlresolvers import reverse
from product_details import product_details


product_languages_lower = dict((locale.lower(), data) for locale, data in
                               product_details.languages.items())
"""
Stores info about languages from product_details using lower-cased locale names
(because the DB stores locales in that format).
"""


def absolutify(url, protocol=None, cdn=False):
    """
    Return the given url with an added domain and protocol. Uses
    settings.SITE_URL to determine the default domain and protocol.

    Use protocol to specify a protocol, cdn=True to use settings.CDN_DOMAIN as
    the domain.
    """
    parsed_site_url = urlparse(settings.SITE_URL)

    if cdn and settings.CDN_DOMAIN:
        domain = settings.CDN_DOMAIN
    else:
        domain = parsed_site_url.netloc

    if protocol is None:
        protocol = parsed_site_url.scheme

    # Add : to protocol unless protocol is blank (relative protocols)
    if protocol != '':
        protocol = '%s:' % protocol

    return ''.join((protocol, '//', domain, url))


def unicode_choice_sorted(choices):
    """
    Sorts a list of 2-tuples by the second value, using a unicode-safe sort.
    """
    return sorted(choices, cmp=lambda x, y: locale_strcoll(x[1], y[1]))


def country_choices():
    """Return a localized, sorted list of tuples of country names and values."""
    items = product_details.get_regions(get_language()).items()
    items.append(('', '---'))  # Empty choice
    return unicode_choice_sorted(items)


def redirect(to, permanent=False, anchor=None, **kwargs):
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

    url = reverse(to, **kwargs)
    if anchor:
        url = '#'.join([url, anchor])

    return redirect_class(url)


def current_locale():
    """
    Return the current Locale object (from Babel). Defaults to en-US if locale
    does not exist.
    """
    try:
        return Locale.parse(get_language(), sep='-')
    except (UnknownLocaleError, ValueError):
        # Default to en-US
        return Locale('en', 'US')


def ugettext_locale(message, locale):
    """Translate a message in a specific locale."""
    old_locale = get_language()
    tower.activate(locale)
    text = tower.ugettext(message)
    tower.activate(old_locale)

    return text


reverse_lazy = lazy(reverse, unicode)


def get_object_or_none(klass, *args, **kwargs):
    """
    Runs klass.objects.get with the given arguments and returns None if no
    matching object is found.
    """
    try:
        return klass.objects.get(*args, **kwargs)
    except (klass.DoesNotExist, klass.MultipleObjectsReturned):
        return None
