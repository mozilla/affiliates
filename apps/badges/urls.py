from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('badges.views',
    url(r'^$', 'home', name='home'),
)
