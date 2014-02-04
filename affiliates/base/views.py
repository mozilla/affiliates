from django.shortcuts import render
from django.views.defaults import page_not_found, server_error

from commonware.response.decorators import xframe_allow

from affiliates.facebook.utils import in_facebook_app


def landing(request):
    return render(request, 'base/landing.html')


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
