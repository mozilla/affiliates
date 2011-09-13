from django.contrib.sites.models import Site
from django.utils.translation import get_language

from product_details import product_details


def absolutify(url, https=False):
    protocol = 'http://' if not https else 'https://'
    domain = Site.objects.get_current().domain
    return ''.join((protocol, domain, url))


# TODO: Sort unicode-aware once localized countries are actually being used.
def country_choices():
    """Return a localized, sorted list of tuples of country names and values."""
    items = product_details.get_regions(get_language()).items()
    return sorted(items, key=lambda x: x[1])
