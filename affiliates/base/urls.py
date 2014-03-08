from django.conf.urls import patterns, url

from affiliates.base import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='base.home'),
    url(r'^dashboard/$', views.dashboard, name='base.dashboard'),
    url(r'^leaderboard/$', views.leaderboard, name='base.leaderboard'),
)
