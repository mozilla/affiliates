from django.conf import settings
from django.db import models

from tower import ugettext_lazy as _lazy

from badges.models import Badge, BadgeInstance, ModelBase
from funfactory.utils import absolutify


class Banner(Badge):
    """Badge consisting of an image link."""
    customize_view = 'banners.views.customize_banner'

    def image_url_dict(self):
        """
        Return a dictionary that maps sizes and colors to the fully qualified
        URLs of this banner's images.
        """
        img_urls = {}
        for img in self.bannerimage_set.all():
            if img.size not in img_urls:
                img_urls[img.size] = {}

            img_urls[img.size][img.color] = absolutify(img.image.url)

        return img_urls

    def image_size_color_dict(self):
        """
        Return a dict that maps sizes to colors available for those sizes
        from all of this banner's images.
        """
        size_colors = {}
        for img in self.bannerimage_set.all():
            if img.size not in size_colors:
                size_colors[img.size] = []
            size_colors[img.size].append(img.color)

        return size_colors


class BannerImage(ModelBase):
    """Image that a user can choose for their specific banner."""
    banner = models.ForeignKey(Banner)
    size = models.CharField(max_length=20, verbose_name=_lazy(u'image size'))
    color = models.CharField(max_length=20, verbose_name=_lazy(u'image color'))
    image = models.ImageField(upload_to=settings.BANNER_IMAGE_PATH,
                              verbose_name=_lazy(u'image file'),
                              max_length=settings.MAX_FILEPATH_LENGTH)

    def __unicode__(self):
        return '%s: %s %s' % (self.banner.name, self.color, self.size)


class BannerInstance(BadgeInstance):
    banner = models.ForeignKey(Banner)
    image = models.ForeignKey(BannerImage)

    def __unicode__(self):
        return '%s: %s' % (self.user, self.image)
