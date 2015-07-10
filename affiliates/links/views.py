from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin
from csp.decorators import csp_exempt

from affiliates.links.models import Link
from affiliates.links.tasks import add_click


class LinkDetailView(LoginRequiredMixin, DetailView):
    template_name = 'links/detail.html'
    context_object_name = 'link'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class LinkReferralView(DetailView):
    template_name = 'links/referral.html'
    context_object_name = 'link'
    queryset = Link.objects.select_related('user')

    @csp_exempt
    @never_cache
    def dispatch(self, *args, **kwargs):
        return super(LinkReferralView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = super(LinkReferralView, self).get(request, *args, **kwargs)
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        key = '{0}_clicked'.format(remote_addr)
        count = cache.get(key, 0)
        if count < settings.MAX_CLICK_COUNT:
            if count == 0:
                cache.set(key, 1, settings.CLICK_THROTTLE_TIMEOUT)
            else:
                cache.incr(key)
            add_click.delay(self.object.id, timezone.now().date())
        return response


class LegacyLinkReferralView(LinkReferralView):
    def get_object(self, queryset=None):
        links = Link.objects.filter(user__id=self.kwargs['user_id'],
                                    legacy_banner_image_id=self.kwargs['banner_img_id'])
        if not links:
            raise Http404()
        else:
            return links[0]
