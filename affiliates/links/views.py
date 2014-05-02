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
    def dispatch(self, *args, **kwargs):
        return super(LinkReferralView, self).dispatch(*args, **kwargs)
