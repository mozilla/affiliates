from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import jingo
from caching.base import CachingManager, CachingMixin, CachingQuerySet
from funfactory.manage import path
from tower import ugettext_lazy as _lazy

from badges.models import Badge, BadgeInstance, LocaleField, ModelBase
from shared.utils import absolutify

# L10n: Width and height are the width and height of an image.
SIZE = _lazy('%(width)sx%(height)s pixels')


BANNER_TEMPLATE_FILE = 'apps/banners/templates/banners/banner_template.html'
with open(path(BANNER_TEMPLATE_FILE)) as f:
    BANNER_TEMPLATE = f.read()


class Banner(Badge):
    """Badge consisting of an image link."""
    customize_view = 'banners.views.customize_banner'

    objects = CachingManager()

    def customize_url(self):
        return reverse('banners.customize', kwargs={'banner_pk': self.pk})


class BannerImageQuerySet(CachingQuerySet):
    def size_color_to_image_map(self):
        """
        Return a dictionary that maps sizes and colors to these banner images.
        """
        banner_images = {}
        for img in self:
            if img.size not in banner_images:
                banner_images[img.size] = {}

            banner_images[img.size][img.color] = {
                'image_url': absolutify(img.image.url, cdn=True),
                'pk': img.pk
            }

        return banner_images

    def size_to_color_map(self):
        """
        Return a dict that maps sizes to colors available for those sizes.
        """
        size_colors = {}
        for img in self:
            if img.size not in size_colors:
                size_colors[img.size] = []
            size_colors[img.size].append(img.color)

        return size_colors


class BannerImageManager(CachingManager):
    def get_query_set(self):
        """Overrides the default QuerySet class with a custom one."""
        return BannerImageQuerySet(self.model, using=self._db)


class BannerImage(CachingMixin, ModelBase):
    """Image that a user can choose for their specific banner."""
    banner = models.ForeignKey(Banner)
    color = models.CharField(max_length=20, verbose_name=_lazy(u'image color'))
    image = models.ImageField(upload_to=settings.BANNER_IMAGE_PATH,
                              verbose_name=_lazy(u'image file'),
                              max_length=settings.MAX_FILEPATH_LENGTH)
    locale = LocaleField()

    objects = BannerImageManager()

    @property
    def size(self):
        """Return a string representing the size of this image in pixels."""
        if self.image:
            return SIZE % {'width': self.image.width,
                           'height': self.image.height}
        else:
            return u''

    def __unicode__(self):
        return '%s: %s %s' % (self.banner.name, self.color, self.size)


class BannerInstance(BadgeInstance):
    image = models.ForeignKey(BannerImage)

    details_template = 'banners/details.html'

    def render(self):
        return jingo.env.from_string(BANNER_TEMPLATE).render({
            'url': self.affiliate_link(),
            'img': absolutify(self.image.image.url)
        })

    def affiliate_link(self):
        return reverse('banners.link', kwargs={'user_id': self.user.pk,
                                               'banner_id': self.badge.pk,
                                               'banner_img_id': self.image.pk})
