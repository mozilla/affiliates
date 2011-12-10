import json
import logging
import socket

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from badges.views import dashboard
from banners import tasks
from banners.urls import AFFILIATE_LINK
from banners.models import Banner, BannerImage, BANNER_TEMPLATE
from shared.decorators import login_required


CACHE_LINK_INSTANCE = 'banner_link_instance_%s_%s'


log = logging.getLogger('a.banners')


@login_required
def customize(request, banner_pk=None):
    banner = get_object_or_404(Banner, pk=banner_pk)
    affiliate_link = AFFILIATE_LINK % (request.user.pk, banner.pk)
    banner_images = [{
        'pk': img.pk,
        'size': img.size,
        'color': img.color,
        'url': img.image.url,
        'language': settings.LANGUAGES[img.locale]
    } for img in BannerImage.objects.filter(banner=banner)]

    return dashboard(request, 'banners/customize.html',
                        {'banner': banner,
                         'affiliate_link': affiliate_link,
                         'subcategory': banner.subcategory,
                         'template': BANNER_TEMPLATE,
                         'banner_images': json.dumps(banner_images)})


@never_cache
def link(request, user_id, banner_id, banner_img_id):
    try:
        banner = Banner.objects.get(pk=banner_id)
    except Banner.DoesNotExist:
        return HttpResponseRedirect(settings.DEFAULT_AFFILIATE_LINK)

    try:
        tasks.add_click.delay(user_id, banner_id, banner_img_id)
    except socket.timeout:
        log.warning('Timeout connecting to celery for banner click.')

    return HttpResponseRedirect(banner.href)
