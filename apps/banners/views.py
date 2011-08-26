import json

from badges.utils import affiliate_link_render
from badges.views import dashboard
from banners.urls import AFFILIATE_LINK
from banners.models import Banner, BannerImage, BannerInstance, BANNER_TEMPLATE


def customize(request, banner_pk=None):
    banner = Banner.objects.select_related().get(pk=banner_pk)
    json_banner_images = json.dumps(banner.banner_image_dict())
    json_size_colors = json.dumps(banner.image_size_color_dict())
    affiliate_link = AFFILIATE_LINK % (request.user.pk, banner.pk)

    return dashboard(request, 'banners/customize.html',
                        {'banner': banner,
                         'affiliate_link': affiliate_link,
                         'subcategory': banner.subcategory,
                         'template': BANNER_TEMPLATE,
                         'json_banner_images': json_banner_images,
                         'json_size_colors': json_size_colors})


def link(request, user_id, banner_id, banner_img_id):
    instance, created = BannerInstance.objects.select_related().get_or_create(
        user_id=user_id, badge_id=banner_id, image_id=banner_img_id)

    if created:
        banner_img = BannerImage.objects.select_related().get(pk=banner_img_id)
        instance.badge = banner_img.banner
        instance.save()

    return affiliate_link_render(request, instance)
