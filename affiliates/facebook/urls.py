from django.conf.urls import patterns, url

from affiliates.facebook import views
from affiliates.shared.views import handler404, handler500


urlpatterns = patterns('affiliates.facebook.views',
    url(r'^/?$', views.load_app, name='facebook.load_app'),

    url(r'^pre_auth/?$', views.pre_auth_promo, name='facebook.pre_auth_promo'),

    url(r'^banners/new/?$', views.banner_create,
        name='facebook.banner_create'),

    url(r'^banners/?$', views.banner_list, name='facebook.banner_list'),

    url(r'^banners/(\d+)/create_image_check/?$',
        views.banner_create_image_check,
        name='facebook.banners.create_image_check'),

    url(r'^banners/(\d+)/share/?$', views.banner_share,
        name='facebook.banners.share'),

    url(r'^post_banner_share/?$', views.post_banner_share,
        name='facebook.post_banner_share'),

    url(r'^banners/delete/?$', views.banner_delete,
        name='facebook.banners.delete'),

    url(r'^links/create/?$', views.link_accounts,
        name='facebook.link_accounts'),

    url(r'^links/([0-9A-Za-z]+-[0-9A-Za-z]+)/activate/?$', views.activate_link,
        name='facebook.links.activate'),

    url(r'^links/remove/?$', views.remove_link,
        name='facebook.links.remove'),

    url(r'^banners/(\d+)/link/?$', views.follow_banner_link,
        name='facebook.banners.link'),

    url(r'^leaderboard/?$', views.leaderboard, name='facebook.leaderboard'),

    url(r'^faq/?$', views.faq, name='facebook.faq'),

    url(r'^invite/?$', views.invite, name='facebook.invite'),

    url(r'^invite/done/?$', views.post_invite, name='facebook.post_invite'),

    url(r'^newsletter/subscribe/?$', views.newsletter_subscribe,
        name='facebook.newsletter.subscribe'),

    url(r'^stats/(\d+|:year:)/(\d+|:month:)/?$', views.stats, name='facebook.stats'),

    url(r'^deauthorize/?$', views.deauthorize, name='facebook.deauthorize'),

    url(r'^404/?$', handler404, name='facebook.404'),

    url(r'^500/?$', handler500, name='facebook.500'),

    url(r'^safari_workaround/?$', views.safari_workaround,
        name='facebook.safari_workaround'),
)
