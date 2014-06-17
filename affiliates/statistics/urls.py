from django.conf.urls import patterns, url

from affiliates.statistics import views


urlpatterns = patterns('',
    url(r'^statistics/$', views.index, name='statistics.index'),
    url(r'^statistics/category/(?P<pk>\d+)/$', views.CategoryDetailView.as_view(),
        name='statistics.category'),
)
