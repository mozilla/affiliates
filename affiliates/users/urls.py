from django.conf.urls import patterns, url

from affiliates.users import views


urlpatterns = patterns('',
    url(r'^profile/(?P<pk>\d+)/$', views.UserProfileView.as_view(), name='users.profile'),
)
