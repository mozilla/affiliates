from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.defaults import page_not_found, server_error

import basket
import commonware
from commonware.response.decorators import xframe_allow
from django_browserid.views import Verify
from tower import ugettext as _

from affiliates.base.forms import NewsletterSubscriptionForm
from affiliates.base.http import JSONResponse
from affiliates.base.utils import redirect
from affiliates.facebook.utils import in_facebook_app
from affiliates.links.models import Link


log = commonware.log.getLogger('a.facebook')


def home(request):
    if request.user.is_authenticated():
        return redirect('base.dashboard')
    else:
        return render(request, 'base/home.html', {
            'affiliate_count': User.objects.count(),
            'link_count': Link.objects.count(),
            'click_count': Link.objects.total_link_clicks(),
        })

def about(request):
    return render(request, 'base/about.html')

def terms(request):
    return render(request, 'base/terms.html')

@login_required
def dashboard(request):
    # Replace request.user and prefetch related items that we need.
    request.user = (User.objects
                    .prefetch_related('link_set__datapoint_set',
                                      'link_set__banner_variation')
                    .get(pk=request.user.pk))

    # Sort links in python to use prefetched data
    links = sorted(request.user.link_set.all(), lambda x, y: cmp(x.created, y.created))

    return render(request, 'base/dashboard.html', {
        'links': links,
    })


@require_POST
def newsletter_subscribe(request):
    form = NewsletterSubscriptionForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        try:
            basket.subscribe(data['email'], 'affiliates',
                             format=data['format'], country=data['country'],
                             source_url=request.build_absolute_uri())
        except basket.BasketException as e:
            log.error('Error subscribing email {0} to mailing list: {1}'.format(data['email'], e))
            return JSONResponse({'error': 'basket_error'}, status=500)

    return JSONResponse({'success': 'success'})


@xframe_allow
def handler404(request):
    if in_facebook_app(request):
        return render(request, 'facebook/error.html', status=404)
    else:
        return page_not_found(request)


@xframe_allow
def handler500(request):
    if in_facebook_app(request):
        return render(request, 'facebook/error.html', status=500)
    else:
        return server_error(request)


def strings(request):
    return render(request, 'base/strings.html')


class BrowserIDVerify(Verify):
    def login_failure(self, msg=None):
        if not msg:
            msg = _('Login failed. Firefox Affiliates has stopped accepting new users.')
        messages.error(self.request, msg)
        return JSONResponse({'redirect': self.failure_url})
