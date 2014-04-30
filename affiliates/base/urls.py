from django.conf.urls import patterns, url

from affiliates.base import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='base.home'),
    url(r'^dashboard/$', views.dashboard, name='base.dashboard'),
    url(r'^about/$', views.about, name='base.about'),
    url(r'^terms/$', views.terms, name='base.terms'),
    url(r'^newsletter/subscribe/$', views.newsletter_subscribe, name='base.newsletter_subscribe'),
    url(r'^strings/$', views.strings, name='base.strings'),
)
