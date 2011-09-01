from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.functional import lazy


reverse_lazy = lazy(reverse, str)


def handle_affiliate_link(badge_instance):
    """
    Record an affiliate link click and redirect to the proper URL.
    """
    badge_instance.add_click()

    return HttpResponseRedirect(badge_instance.badge.href)
