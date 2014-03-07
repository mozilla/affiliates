from urlparse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.translation import get_language

from babel.core import Locale, UnknownLocaleError
from funfactory.urlresolvers import reverse
from product_details import product_details


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


def get_object_or_none(klass, *args, **kwargs):
    """
    Runs klass.objects.get with the given arguments and returns None if no
    matching object is found.
    """
    try:
        return klass.objects.get(*args, **kwargs)
    except (klass.DoesNotExist, klass.MultipleObjectsReturned):
        return None


LOCALE_TO_NATIVE = dict([(key.lower(), value['native']) for key, value in
                         product_details.languages.items()])


def locale_to_native(locale):
    """Return the native name for the given locale."""
    return LOCALE_TO_NATIVE.get(locale)
