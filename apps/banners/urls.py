from django.conf.urls.defaults import patterns, url

from shared.utils import absolutify


# Reverse won't let us use placeholder values (so Javascript can replace the
# banner_img_id), so we store this link as a string.
AFFILIATE_LINK = absolutify('/link/banner/%s/%s/{{ banner_img_id }}',
                            https=True)


urlpatterns = patterns('banners.views',
    url(r'^banners/customize/(?P<banner_pk>\d+)$', 'customize',
        name='banners.customize'),
    url(r'^link/banner/(?P<user_id>\d+)/(?P<banner_id>\d+)/(?P<banner_img_id>\d+)$',
        'old_link', name='banners.link.old'),
    url(r'^link/banner/(?P<banner_instance_id>\d+)$', 'link', name='banners.link'),
)
