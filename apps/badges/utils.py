from django.conf import settings
from django.contrib.sites.models import Site


def fq_url(absolute_path, https=False):
    """
    Return a fully qualified URL including the current domain for the given
    absolute path.
    """
    domain = Site.objects.get_current().domain
    if settings.SERVER_PORT is not None:
        domain = '%s:%s' % (domain, settings.SERVER_PORT)

    if https:
        prefix = 'https'
    else:
        prefix = 'http'

    return '%s://%s%s' % (prefix, domain, absolute_path)
