from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse

from shared.decorators import login_required


@login_required
def mock_view(request, *args, **kwargs):
    return HttpResponse('test')


def mock_login_view(request, *args, **kwargs):
    return HttpResponse('test_login')


urlpatterns = patterns('',
    url(r'^mock_view$', mock_view, name='mock_view'),
    url(r'^mock_login_view$', mock_login_view, name='mock_login_view'),
)
