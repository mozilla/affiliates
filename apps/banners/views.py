import json

import jingo

from banners.models import Banner


BANNER_TEMPLATE_FILE = 'banners/banner_template.html'
BANNER_TEMPLATE = jingo.env.get_template(BANNER_TEMPLATE_FILE).render()


def customize_banner(request, pk=None):
    banner = Banner.objects.select_related().get(pk=pk)
    json_banner_urls = json.dumps(banner.image_url_dict())
    json_size_colors = json.dumps(banner.image_size_color_dict())

    return jingo.render(request, 'banners/customize.html',
                        {'banner': banner,
                         'subcategory': banner.subcategory,
                         'template': BANNER_TEMPLATE,
                         'json_banner_images': json_banner_urls,
                         'json_size_colors': json_size_colors})
