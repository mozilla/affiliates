from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from funfactory.monkeypatches import patch

from affiliates.shared.admin import admin_site


# Apply funfactory monkeypatches.
patch()

admin.autodiscover()

handler404 = 'affiliates.shared.views.view_404'
handler500 = 'affiliates.shared.views.view_500'


urlpatterns = patterns('',
    (r'', include('affiliates.shared.urls')),
    (r'', include('affiliates.badges.urls')),
    (r'', include('affiliates.banners.urls')),
    (r'^accounts/', include('affiliates.users.urls')),
    (r'^browserid/', include('affiliates.browserid.urls')),
    (r'^fb/', include('affiliates.facebook.urls')),

    (r'^admin/', include('smuggler.urls')),
    (r'^admin/', include(admin_site.urls)),
)


# In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^404/$', handler404),
        (r'^500/$', handler500),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
