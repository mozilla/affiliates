from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('shared.views',
    url(r'^$', 'home', name='home'),
    url(r'^about$', 'about', name='about'),
    url(r'^faq$', 'faq', name='faq'),
    url(r'^tos$', direct_to_template, {'template': 'shared/tos.html'},
        name='tos'),
    url(r'^404$', 'view_404', name='404'),
    url(r'^500$', 'view_500', name='500'),
    url(r'^newsletter/subscribe/?$', 'newsletter_subscribe',
        name='shared.newsletter.subscribe'),
)
