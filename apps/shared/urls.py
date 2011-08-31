from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('shared.views',
    url(r'^about$', 'about', name='about'),
    url(r'^faq$', 'faq', name='faq'),
)
