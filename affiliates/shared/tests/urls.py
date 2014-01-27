from django.conf.urls import patterns, url
from django.http import HttpResponse


def mock_view(request, *args, **kwargs):
    return HttpResponse('test')


urlpatterns = patterns('',
    url(r'^mock_view$', mock_view, name='mock_view'),
)
