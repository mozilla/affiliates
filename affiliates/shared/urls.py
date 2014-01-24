from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('affiliates.shared.views',
    url(r'^$', 'home', name='home'),
    url(r'^about$', 'about', name='about'),
    url(r'^faq$', 'faq', name='faq'),
    url(r'^tos$', TemplateView.as_view(template_name='shared/tos.html'), name='tos'),
    url(r'^404$', 'view_404', name='404'),
    url(r'^500$', 'view_500', name='500'),
    url(r'^newsletter/subscribe/?$', 'newsletter_subscribe', name='shared.newsletter.subscribe'),
)
