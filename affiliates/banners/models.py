import hashlib
import os

from django.conf import settings
from django.db import models

from funfactory.manage import path

from affiliates.badges.models import Badge, BadgeInstance
from affiliates.banners import COLOR_CHOICES
from affiliates.shared.models import LocaleField, ModelBase


BANNER_TEMPLATE_FILE = 'affiliates/banners/templates/banners/banner_template.html'
with open(path(BANNER_TEMPLATE_FILE)) as f:
    BANNER_TEMPLATE = f.read()


def rename(instance, filename):
    props = '%d_%s_%s_%s_%s' % (instance.banner_id,
                                instance.image.width,
                                instance.image.height,
                                instance.color,
                                instance.locale)
    hash = hashlib.sha1(props).hexdigest()
    extension = os.path.splitext(filename)[1]
    name = '%s%s' % (hash, extension)
    return os.path.join(settings.BANNER_IMAGE_PATH, name)


class Banner(Badge):
    """Badge consisting of an image link."""
    customize_view = 'banners.views.customize_banner'


class BannerImage(ModelBase):
    """Image that a user can choose for their specific banner."""
    banner = models.ForeignKey(Banner)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES,
                             verbose_name=u'image color')
    image = models.ImageField(upload_to=rename,
                              verbose_name=u'image file',
                              max_length=settings.MAX_FILEPATH_LENGTH)
    locale = LocaleField()

    def __unicode__(self):
        return '%s: %s %s' % (self.banner.name, self.color, self.size)


class BannerInstance(BadgeInstance):
    image = models.ForeignKey(BannerImage)
