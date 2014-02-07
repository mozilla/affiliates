from django.conf.urls import patterns, url

from affiliates.banners import views


urlpatterns = patterns('',
    url(r'^generator/categories/$', views.CategoryListView.as_view(),
        name='banners.generator.categories'),

    url(r'^generator/categories/(?P<category_pk>\d+)/$', views.BannerListView.as_view(),
        name='banners.generator.banners'),

    url(r'^generator/image_banners/(?P<pk>\d+)/customize/$',
        views.CustomizeImageBannerView.as_view(), name='banners.generator.image_banner.customize'),
)
