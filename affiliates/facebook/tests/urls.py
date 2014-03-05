from django.conf.urls import include, patterns, url
from django.http import HttpResponse
from django.template import RequestContext

from jingo import env


def base_template_view(request):
    template = env.from_string("""
        {% extends 'facebook/base.html' %}
        {% block content %}test{% endblock %}
    """)
    return HttpResponse(template.render(RequestContext(request)))


urlpatterns = patterns('',
    # Include base urls to avoid NoReverseMatch errors.
    (r'', include('affiliates.urls')),

    url('^fb/test$', base_template_view, name='facebook.base_test'),
)
