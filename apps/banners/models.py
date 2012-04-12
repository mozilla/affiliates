import hashlib
import os

from django.conf import settings
from django.db import models

import jingo
from caching.base import CachingManager, CachingMixin
from funfactory.manage import path
from funfactory.urlresolvers import reverse
from jinja2 import Markup
from tower import ugettext_lazy as _lazy

from badges.models import Badge, BadgeInstance
from banners import COLOR_CHOICES
from shared.models import LocaleField, ModelBase
from shared.storage import OverwritingStorage
from shared.utils import absolutify, ugettext_locale as _locale


# L10n: Width and height are the width and height of an image.
SIZE = _lazy('%(width)sx%(height)s pixels')


BANNER_TEMPLATE_FILE = 'apps/banners/templates/banners/banner_template.html'
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

    objects = CachingManager()

    def customize_url(self):
        return reverse('banners.customize', kwargs={'banner_pk': self.pk})


class BannerImageManager(CachingManager):
    def customize_values(self, **kwargs):
        """Retrieve data needed for banner customization."""
        return [{
            'pk': img.pk,
            'size': img.size,
            'area': img.image.width * img.image.height,
            'color': img.color,
            'url': img.image.url,
            'language': settings.LANGUAGES[img.locale]
            } for img in self.filter(**kwargs)]


class BannerImage(CachingMixin, ModelBase):
    """Image that a user can choose for their specific banner."""
    banner = models.ForeignKey(Banner)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES,
                             verbose_name=u'image color')
    image = models.ImageField(upload_to=rename,
                              storage=OverwritingStorage(),
                              verbose_name=u'image file',
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
    objects = CachingManager()

    @property
    def preview(self):
	"""Return the HTML to preview this banner."""
	return Markup('<img src="%s?from_affiliates" alt="%s">' % (absolutify(self.image.image.url, cdn=True),
						   _locale(self.badge.name, self.image.locale)))

    @property
    def code(self):
        """Return the code to embed this banner.."""
        return jingo.env.from_string(BANNER_TEMPLATE).render({
            'url': self.affiliate_link(),
	    'img': absolutify(self.image.image.url, cdn=True),
            'alt_text': _locale(self.badge.name, self.image.locale)
        })

    def affiliate_link(self):
        link = reverse('banners.link', kwargs={'banner_instance_id': self.pk})
        return absolutify(link)
