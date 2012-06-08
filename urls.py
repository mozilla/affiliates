from urlparse import urlparse

from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin

from funfactory.admin import site as patched_site

from stats.monkeypatches import patch

# TODO: Remove once Affiliates is upgraded to the latest funfactory, as it
# patches this.
admin.site = patched_site  # Patch with session_csrf fix

# Patch admin site for stats application
patch(admin.site)
admin.autodiscover()

handler404 = 'shared.views.view_404'
handler500 = 'shared.views.view_500'

urlpatterns = patterns('',
    (r'', include('shared.urls')),
    (r'', include('badges.urls')),
    (r'', include('banners.urls')),
    (r'^accounts/', include('users.urls')),
    (r'^browserid/', include('browserid.urls')),
    (r'^fb/', include('facebook.urls')),


    (r'^admin/', include('smuggler.urls')),
    (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG or settings.SERVE_MEDIA:
    # Remove host, leading and trailing slashes so the regex matches.
    media_url = urlparse(settings.MEDIA_URL).path.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
