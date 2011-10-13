import json

from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from django.views.decorators.cache import never_cache

from badges.utils import handle_affiliate_link
from badges.views import dashboard
from banners.urls import AFFILIATE_LINK
from banners.models import Banner, BannerImage, BannerInstance, BANNER_TEMPLATE
from shared.decorators import login_required


CACHE_LINK_INSTANCE = 'banner_link_instance_%s_%s'


@login_required
def customize(request, banner_pk=None):
    banner = get_object_or_404(Banner, pk=banner_pk)
    banner_images = banner.bannerimage_set.filter(locale=get_language())

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


# TODO: Remove need for banner_id in link
@never_cache
def link(request, user_id, banner_id, banner_img_id):
    try:
        banner_img = (BannerImage.objects.select_related('Banner')
                      .get(pk=banner_img_id))
    except BannerImage.DoesNotExist:
        return HttpResponseRedirect(settings.DEFAULT_AFFILIATE_LINK)

    key = CACHE_LINK_INSTANCE % (user_id, banner_img_id)
    instance = cache.get(key)
    if instance is None:
        try:
            instance, created = (BannerInstance.objects.select_related('badge')
                                 .get_or_create(user_id=user_id,
                                                badge=banner_img.banner,
                                                image=banner_img))
            cache.set(key, instance)
        except IntegrityError:
            return HttpResponseRedirect(settings.DEFAULT_AFFILIATE_LINK)

    return handle_affiliate_link(instance)
