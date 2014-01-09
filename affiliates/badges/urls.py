from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('affiliates.badges.views',
    url(r'^my_banners$', 'my_badges', name='my_badges'),
    url(r'^new$', 'new_badge_step1', name='badges.new.step1'),
    url(r'^new/(?P<subcategory_pk>\d+)$', 'new_badge_step2',
        name='badges.new.step2'),
    url(r'^stats/(\d+|:month:)/(\d+|:year:)$', 'month_stats_ajax', name='badges.ajax.stats'),
)
