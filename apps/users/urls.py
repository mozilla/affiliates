from django.contrib.auth.views import logout
from django.conf.urls.defaults import patterns, url

from shared.utils import reverse_lazy
from users import views


urlpatterns = patterns('',
    url(r'^login/?$', views.login, name='users.login'),
    url(r'^logout/?$', logout, {'next_page': reverse_lazy('home')},
        name='users.logout'),
    url(r'^register$', views.register, name='users.register'),
    url(r'^edit$', views.edit_profile, name='users.edit.profile'),
    url(r'^activate/(?P<activation_key>\w+)$', views.activate,
        name='users.activate'),
    url(r'^forgot_password$', views.send_password_reset,
        name='users.send_password_reset'),
    url(r'^pwreset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)$',
        views.password_reset, name="users.password_reset"),
)
