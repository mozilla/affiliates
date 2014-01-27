from django.conf.urls import patterns, url

from affiliates.base import views


urlpatterns = patterns('',
    url(r'^$', views.landing, name='base.landing'),
)
