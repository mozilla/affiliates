from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib.admin import autodiscover

from funfactory import admin

from stats.monkeypatches import patch


# Patch admin site for stats application
patch(admin.site)

autodiscover()

urlpatterns = patterns('',
    (r'', include('shared.urls')),
    (r'', include('badges.urls')),
    (r'', include('banners.urls')),
    (r'^accounts/', include('users.urls')),
    (r'^browserid/', include('browserid.urls')),

    (r'^admin/', include('smuggler.urls')),
    (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG or settings.SERVE_MEDIA:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
