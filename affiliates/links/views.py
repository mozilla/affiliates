from django.http import Http404
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin
from csp.decorators import csp_exempt

from affiliates.links.models import Link


class LinkDetailView(LoginRequiredMixin, DetailView):
    template_name = 'links/detail.html'
    context_object_name = 'link'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class LinkReferralView(DetailView):
    template_name = 'links/referral.html'
    model = Link
    context_object_name = 'link'

    @csp_exempt
    @never_cache
    def dispatch(self, *args, **kwargs):
        return super(LinkReferralView, self).dispatch(*args, **kwargs)


class LegacyLinkReferralView(LinkReferralView):
    def get_object(self, queryset=None):
        links = Link.objects.filter(user__id=self.kwargs['user_id'],
                                    legacy_banner_image_id=self.kwargs['banner_img_id'])
        if not links:
            raise Http404()
        else:
            return links[0]
