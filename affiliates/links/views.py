from django.views.generic import DetailView

from braces.views import LoginRequiredMixin

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
