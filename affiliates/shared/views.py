from django.shortcuts import render
from django.views.defaults import server_error

from affiliates.facebook.utils import in_facebook_app


def view_404(request):
    template = '404.html'
    if in_facebook_app(request):
        template = 'facebook/error.html'

    return render(request, template, status=404)


def view_500(request):
    if in_facebook_app(request):
        return render(request, 'facebook/error.html', status=500)
    else:
        return server_error(request)
