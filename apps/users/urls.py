from django.conf.urls.defaults import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^register$', views.register, name='users.register'),
    url(r'^activate/(?P<activation_key>\w+)$', views.activate,
        name='users.activate'),
)
