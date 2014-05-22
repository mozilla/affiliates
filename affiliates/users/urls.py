from django.conf.urls import patterns, url
from django.views.decorators.cache import never_cache

from django_browserid.views import CsrfToken

from affiliates.users import views


urlpatterns = patterns('',
    url(r'^profile/(?P<pk>\d+)/$', views.UserProfileView.as_view(), name='users.profile'),
    url(r'^login_required/$', views.login_required, name='users.login_required'),

    # Temporary workaround for bug 1014273: Do not cache CSRFToken view.
    # We override the django_browserid version by coming first in the
    # URLConf.
    url(r'^browserid/csrf/$', never_cache(CsrfToken.as_view())),
)
