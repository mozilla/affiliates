from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from affiliates.links import views


urlpatterns = patterns('',
    # Old banner links started with '/link/', so we can't use '/link/'
    # for normal site URLs as the `/link/` prefix is included in
    # SUPPORTED_NONLOCALES.
    url(r'^links/(?P<pk>\d+)/$', views.LinkDetailView.as_view(), name='links.detail'),

    url(r'^referral/(?P<pk>\d+)/$', views.LinkReferralView.as_view(), name='links.referral'),
    url(r'^link/banner/(?P<pk>\d+)/$', views.LinkReferralView.as_view(),
        name='links.referral.old'),
    url(r'^link/banner/(?P<user_id>\d+)/(?P<banner_id>\d+)/(?P<banner_img_id>\d+)/$',
        views.LegacyLinkReferralView.as_view(), name='links.referral.older'),

    url(r'^leaderboard/$', TemplateView.as_view(template_name='links/leaderboard.html'),
        name='links.leaderboard'),
)
