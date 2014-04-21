from django.conf.urls import patterns, url

from affiliates.users import views


urlpatterns = patterns('',
    url(r'^profile/(?P<pk>\d+)/$', views.UserProfileView.as_view(), name='users.profile'),
    url(r'^login_required/$', views.login_required, name='users.login_required'),
)
