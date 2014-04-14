from django.conf.urls import patterns, url

from affiliates.base import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='base.home'),
    url(r'^dashboard/$', views.dashboard, name='base.dashboard'),
    url(r'^about/$', views.about, name='base.about'),
    url(r'^terms/$', views.terms, name='base.terms'),

    # TODO: These are static templates; they do not belong here.
    url(r'^embed/$', views.embed, name='base.embed'),
    url(r'^embed_text/$', views.embed_text, name='base.embed_text'),
)
