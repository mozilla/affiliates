from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('affiliates.views',
    url(r'^$', 'home', name='home'),
)
