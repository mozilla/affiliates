from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('badges.views',
    url(r'^$', 'home', name='home'),
    url(r'^new/1$', 'new_badge_step1', name='badges.new.step1'),
    url(r'^new/2$', 'new_badge_step2', name='badges.new.step2'),
    url(r'^new/3$', 'new_badge_step3', name='badges.new.step3'),
)
