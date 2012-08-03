from django.conf.urls.defaults import patterns, url

from facebook import views


urlpatterns = patterns('facebook.views',
    url(r'^/?$', views.load_app, name='facebook.load_app'),
    url(r'^create_banner/?$', views.create_banner, name='facebook.create_banner'),
    url(r'^banner_list/?$', views.banner_list, name='facebook.banner_list'),
    url(r'^post_banner_share/?$', views.post_banner_share,
        name='facebook.post_banner_share'),
)
