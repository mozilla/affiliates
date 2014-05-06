from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.defaults import page_not_found, server_error

import basket
import commonware
from commonware.response.decorators import xframe_allow

from affiliates.base.forms import NewsletterSubscriptionForm
from affiliates.base.http import JSONResponse
from affiliates.base.milestones import MilestoneDisplay
from affiliates.base.models import NewsItem
from affiliates.base.utils import redirect
from affiliates.facebook.utils import in_facebook_app
from affiliates.links.models import DataPoint, Link


log = commonware.log.getLogger('a.facebook')


def home(request):
    if request.user.is_authenticated():
        return redirect('base.dashboard')
    else:
        aggregate_clicks = Link.objects.aggregate(a=Sum('aggregate_link_clicks'))['a'] or 0
        datapoint_clicks = DataPoint.objects.aggregate(d=Sum('link_clicks'))['d'] or 0
        return render(request, 'base/home.html', {
            'affiliate_count': User.objects.count(),
            'link_count': Link.objects.count(),
            'click_count': aggregate_clicks + datapoint_clicks
        })

def about(request):
    return render(request, 'base/about.html')

def terms(request):
    return render(request, 'base/terms.html')

@login_required
def dashboard(request):
    try:
        newsitem = NewsItem.objects.filter(visible=True).latest('created')
    except NewsItem.DoesNotExist:
        newsitem = None

    return render(request, 'base/dashboard.html', {
        'newsitem': newsitem,
        'milestones': MilestoneDisplay(request.user),
        'links': request.user.link_set.order_by('-created'),
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
