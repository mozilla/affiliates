from django.conf.urls import patterns, url

from affiliates.links import views


urlpatterns = patterns('',
    url(r'^link/(?P<pk>\d+)/$', views.LinkDetailView.as_view(), name='links.detail'),
)
