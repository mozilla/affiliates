from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('facebook.views',
    url(r'^/?', 'load_app', name='facebook.load_app'),
)
