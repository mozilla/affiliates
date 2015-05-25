from django.conf.urls import patterns, url

from affiliates.banners import views


urlpatterns = patterns('',
    url(r'^generator/categories/$', views.NoMoreBannersRedirectView.as_view(),
        name='banners.generator.categories'),

    url(r'^generator/categories/(?P<category_pk>\d+)/$', views.NoMoreBannersRedirectView.as_view(),
        name='banners.generator.banners'),

    url(r'^generator/image_banners/(?P<pk>\d+)/customize/$',
        views.NoMoreBannersRedirectView.as_view(), name='banners.generator.image_banner.customize'),

    url(r'^generator/text_banners/(?P<pk>\d+)/customize/$',
        views.NoMoreBannersRedirectView.as_view(), name='banners.generator.text_banner.customize'),

    url(r'^generator/firefox_upgrade_banners/(?P<pk>\d+)/customize/$',
        views.NoMoreBannersRedirectView.as_view(),
        name='banners.generator.firefox_upgrade_banner.customize'),
)
