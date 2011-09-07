from django.contrib.sites.models import Site


def absolutify(url, https=False):
    protocol = 'http://' if not https else 'https://'
    domain = Site.objects.get_current().domain
    return ''.join((protocol, domain, url))
