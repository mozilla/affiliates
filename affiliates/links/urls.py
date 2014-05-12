from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from affiliates.links import views


urlpatterns = patterns('',
    url(r'^link/(?P<pk>\d+)/$', views.LinkDetailView.as_view(), name='links.detail'),
    url(r'^referral/(?P<pk>\d+)/$', views.LinkReferralView.as_view(), name='links.referral'),
    url(r'^link/banner/(?P<pk>\d+)/$', views.LinkReferralView.as_view()),
    url(r'^link/banner/(?P<user_id>\d+)/(?P<banner_id>\d+)/(?P<banner_img_id>\d+)/$',
        views.LegacyLinkReferralView.as_view()),

    url(r'^leaderboard/$', TemplateView.as_view(template_name='links/leaderboard.html'),
        name='links.leaderboard'),
)
