from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.translation import get_language

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


# TODO: Sort unicode-aware once localized countries are actually being used.
def country_choices():
    """Return a localized, sorted list of tuples of country names and values."""
    items = product_details.get_regions(get_language()).items()
    items.append(('', '---'))  # Empty choice
    return sorted(items, key=lambda x: x[1])


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
