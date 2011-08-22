from django.contrib.auth.views import logout
from django.conf.urls.defaults import patterns, url

from badges.utils import reverse_lazy
from users import views


urlpatterns = patterns('',
    url(r'^login$', views.login, name='users.login'),
    url(r'^logout$', logout, {'next_page': reverse_lazy('home')},
        name='users.logout'),
    url(r'^register$', views.register, name='users.register'),
    url(r'^activate/(?P<activation_key>\w+)$', views.activate,
        name='users.activate'),
)
