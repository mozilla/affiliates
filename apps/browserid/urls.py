from django.conf.urls.defaults import patterns, url

from browserid import views


urlpatterns = patterns('',
    url(r'^verify/$', views.verify, name='browserid.verify'),
)
