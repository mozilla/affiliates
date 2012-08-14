from django.conf.urls.defaults import patterns, url

from facebook import views


urlpatterns = patterns('facebook.views',
    url(r'^/?$', views.load_app, name='facebook.load_app'),

    url(r'^create_banner/?$', views.create_banner,
        name='facebook.create_banner'),

    url(r'^banner_list/?$', views.banner_list, name='facebook.banner_list'),

    url(r'^post_banner_share/?$', views.post_banner_share,
        name='facebook.post_banner_share'),

    url(r'^links/create/?$', views.link_accounts,
        name='facebook.link_accounts'),

    url(r'^links/([0-9A-Za-z]+-[0-9A-Za-z]+)/activate/?$', views.activate_link,
        name='facebook.links.activate'),

    url(r'^links/remove/?$', views.remove_link,
        name='facebook.links.remove'),
)
