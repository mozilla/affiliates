from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('shared.views',
    url(r'^$', 'home', name='home'),
    url(r'^about$', 'about', name='about'),
    url(r'^faq$', 'faq', name='faq'),
    url(r'^tos$', direct_to_template, {'template': 'shared/tos.html'},
        name='tos')
)
