from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found, server_error

from commonware.response.decorators import xframe_allow

from affiliates.base.milestones import MilestoneDisplay
from affiliates.base.models import NewsItem
from affiliates.facebook.utils import in_facebook_app


def home(request):
    if request.user.is_authenticated():
        return redirect('base.dashboard')
    else:
        return render(request, 'base/home.html')

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
    })


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
