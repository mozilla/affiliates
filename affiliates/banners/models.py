import hashlib
import os

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string

from mptt.models import MPTTModel, TreeForeignKey

from affiliates.banners import COLOR_CHOICES
from affiliates.base.helpers import media
from affiliates.base.models import LocaleField
from affiliates.base.storage import OverwritingStorage
from affiliates.base.utils import locale_to_native
from affiliates.links.models import Link


class Category(MPTTModel):
    """
    Category that groups together either subcategories or banners.

    A category tree can only be 2 layers deep, including the roots. This
    is only enforced by model validation, so site code could
    theoretically create Categories that violate this rule, but in
    practice the only place that Categories should be created is the
    admin interface.
    """
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def clean(self):
        """
        Validate that this category isn't more than one layer deep.
        """
        if self.get_level() > 1:
            raise ValidationError('Categories cannot be more than one level deep.')

    def __unicode__(self):
        return self.name


class Banner(models.Model):
    """A type of banner that a user can generate links from."""
    category = TreeForeignKey(Category)
    name = models.CharField(max_length=255)
    destination = models.URLField(max_length=255)
    visible = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def generate_banner_code(self, *args, **kwargs):
        """
        Generate the HTML that users will copy onto their website to
        display this banner. Arguments will vary based on the subclass.
        """
        raise NotImplementedError()

    def get_customize_url(self):
        """Generate a URL to the customization page for this banner."""
        raise NotImplementedError()

    def get_banner_type(self):
        """
        Return the value for the banner_type field on Links created by
        this banner.
        """
        raise NotImplementedError()

    def create_link(self, user, **kwargs):
        """
        Create a Link based off of this banner. Extra arguments are
        passed on to generate_banner_code.
        """
        html = self.generate_banner_code(**kwargs)
        link = Link(user=user, destination=self.destination, html='',
                    banner_type=self.get_banner_type())

        # Save to get PK so that link can generate referral URL.
        link.save()
        link.html = html.format(href=link.get_referral_url())
        link.save()

        return link

    def __unicode__(self):
        return self.name


class ImageBanner(Banner):
    """Banner displayed as an image link."""
    def generate_banner_code(self, variation, **kwargs):
        return render_to_string('banners/banner_code/image_banner.html', {
            'variation': variation
        })

    def get_customize_url(self):
        return reverse('banners.generator.image_banner.customize', kwargs={'pk': self.pk})

    def get_banner_type(self):
        return 'image_banner'


class ImageVariation(models.Model):
    """
    Base class for variations of banners that use priarily images in
    their display.

    Child classes _must_ define a ForeignKey field named "banner" that
    points to the banner this variation is categorized under.
    """
    color = models.CharField(max_length=32, choices=COLOR_CHOICES)
    locale = LocaleField()

    def _filename(self, filename):
        props = '{id}_{width}_{height}_{color}_{locale}'.format(
            id=self.banner_id,
            width=self.image.width,
            height=self.image.height,
            color=self.color,
            locale=self.locale
        )
        props_hash = hashlib.sha1(props).hexdigest()
        extension = os.path.splitext(filename)[1]
        return os.path.join(self.get_media_subdirectory(), props_hash + extension)

    image = models.ImageField(upload_to=_filename, max_length=255, storage=OverwritingStorage())

    class Meta:
        abstract = True

    @property
    def size(self):
        return '{width}x{height}'.format(width=self.image.width, height=self.image.height)

    def get_media_subdirectory(self):
        """
        Return the name to use for the subdirectory to store variations
        in, under MEDIA_ROOT.
        """
        raise NotImplementedError()


class ImageBannerVariation(ImageVariation):
    banner = models.ForeignKey(ImageBanner, related_name='variation_set')

    def get_media_subdirectory(self):
        return 'uploads/image_banners'


class TextBanner(Banner):
    """Banner displayed as a string of text with a link."""
    def generate_banner_code(self, variation, **kwargs):
        return u'<a href="{{href}}">{text}</a>'.format(text=variation.text)

    def get_customize_url(self):
        return reverse('banners.generator.text_banner.customize', kwargs={'pk': self.pk})


class TextBannerVariation(models.Model):
    """Localized variation of a text banner."""
    banner = models.ForeignKey(TextBanner, related_name='variation_set')
    text = models.TextField()
    locale = LocaleField()

    def __unicode__(self):
        return locale_to_native(self.locale)

    def generate_banner_code(self, **kwargs):
        return self.text

    def get_banner_type(self):
        return 'text_banner'


class FirefoxUpgradeBanner(Banner):
    """
    Image banner that shows a different image depending on whether the
    viewer has an up-to-date version of Firefox or not.
    """
    def generate_banner_code(self, variation, **kwargs):
        return render_to_string('banners/banner_code/firefox_upgrade_banner.html', {
            'variation': variation
        })

    def get_customize_url(self):
        return reverse('banners.generator.firefox_upgrade_banner.customize',
                       kwargs={'pk': self.pk})


class FirefoxUpgradeBannerVariation(ImageVariation):
    banner = models.ForeignKey(FirefoxUpgradeBanner, related_name='variation_set')

    def _filename(self, filename):
        filename = super(FirefoxUpgradeBannerVariation, self)._filename(filename)
        filename, extension = os.path.splitext(filename)
        return filename + '_upgrade' + extension
    upgrade_image = models.ImageField(upload_to=_filename, max_length=255,
                                      storage=OverwritingStorage())

    def get_media_subdirectory(self):
        return 'uploads/firefox_upgrade_banners'

    @property
    def image_url(self):
        # TODO: Make this URL absolute.
        return media('uploads/upgrade/{pk}'.format(pk=self.pk))
