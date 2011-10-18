import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from badges.views import dashboard
from banners import tasks
from banners.urls import AFFILIATE_LINK
from banners.models import Banner, BANNER_TEMPLATE
from shared.decorators import login_required


CACHE_LINK_INSTANCE = 'banner_link_instance_%s_%s'


@login_required
def customize(request, banner_pk=None):
    banner = get_object_or_404(Banner, pk=banner_pk)
    banner_locale = request.user.get_profile().locale
    banner_images = banner.bannerimage_set.filter(locale=banner_locale)

    # In case of no matches, default to the installation language
    if not banner_images:
        banner_images = (banner.bannerimage_set.
                         filter(locale=settings.LANGUAGE_CODE.lower()))

    json_banner_images = json.dumps(banner_images.size_color_to_image_map())
    json_size_colors = json.dumps(banner_images.size_to_color_map())
    affiliate_link = AFFILIATE_LINK % (request.user.pk, banner.pk)

    return dashboard(request, 'banners/customize.html',
                        {'banner': banner,
                         'affiliate_link': affiliate_link,
                         'subcategory': banner.subcategory,
                         'template': BANNER_TEMPLATE,
                         'json_banner_images': json_banner_images,
                         'json_size_colors': json_size_colors})


@never_cache
def link(request, user_id, banner_id, banner_img_id):
    try:
        banner = Banner.objects.get(pk=banner_id)
    except Banner.DoesNotExist:
        return HttpResponseRedirect(settings.DEFAULT_AFFILIATE_LINK)

    tasks.add_click.delay(user_id, banner_id, banner_img_id)

    return HttpResponseRedirect(banner.href)
