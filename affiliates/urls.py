from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from funfactory.monkeypatches import patch

from affiliates.shared.admin import admin_site


# Apply funfactory monkeypatches.
patch()

admin.autodiscover()


urlpatterns = patterns('',
    (r'', include('affiliates.base.urls')),
    (r'^fb/', include('affiliates.facebook.urls')),

    (r'^admin/', include('smuggler.urls')),
    (r'^admin/', include(admin_site.urls)),
)


# In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
