import os

from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponse
from django.template import RequestContext

from funfactory.manage import ROOT
from jingo import env


def base_template_view(request):
    template = env.from_string("""
        {% extends 'facebook/base.html' %}
        {% block content %}test{% endblock %}
    """)
    return HttpResponse(template.render(RequestContext(request)))


urlpatterns = patterns('',
    # Include base urls to avoid NoReverseMatch errors.
    (r'', include('%s.urls' % os.path.basename(ROOT))),

    url('^fb/test$', base_template_view, name='facebook.base_test'),
)
