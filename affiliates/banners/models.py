import hashlib
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string
from django.utils import translation

from caching.base import CachingManager, CachingMixin
from funfactory.urlresolvers import reverse
from jinja2 import Markup
from mptt.models import MPTTModel, TreeForeignKey

from affiliates.banners import COLOR_CHOICES
from affiliates.base.helpers import media
from affiliates.base.models import LocaleField
from affiliates.base.storage import OverwritingStorage
from affiliates.base.utils import absolutify, locale_to_native
from affiliates.links.models import Link


class Category(CachingMixin, MPTTModel):
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

    objects = CachingManager()

    class Meta:
        verbose_name_plural = 'categories'

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

    def generate_banner_code(self, variation):
        """
        Generate the HTML that users will copy onto their website to
        display this banner.
        """
        raise NotImplementedError()

    def get_customize_url(self):
        """Generate a URL to the customization page for this banner."""
        raise NotImplementedError()

    def preview_html(self, href):
        """
        Render HTML for previewing this banner in a list of banners.
        """
        raise NotImplementedError()

    @staticmethod
    def get_variation_class():
        """
        Return the class object that stores variations of this banner.
        """
        raise NotImplementedError()

    def create_link(self, user, variation):
        """
        Create a Link based off of this banner. Extra arguments are
        passed on to generate_banner_code.
        """
        html = self.generate_banner_code(variation)
        link = Link(user=user, html='', banner_variation=variation)

        # Save to get PK so that link can generate referral URL.
        link.save()
        link.html = html.format(href=link.get_referral_url())
        link.save()

        return link

    def __unicode__(self):
        return self.name


class BannerVariation(models.Model):
    """
    A variation of a banner, typically differing by locale and possibly
    other dimenisons.

    Mostly useful for being explicit about what is expected from a
    variation subclass.
    """
    @property
    def banner(self):
        """The banner that this is a variation of."""
        raise NotImplementedError()

    class Meta:
        abstract = True


class ImageBannerBase(Banner):
    """Common functionality for banners that involve images."""
    preview_template = 'banners/previews/image_banner.html'

    def preview_html(self, href, **kwargs):
        kwargs['href'] = href
        kwargs['banner'] = self

        # Fetch localized variations that are 125x125.
        # Filter in python to take advantage of prefetching.
        locale = translation.get_language()
        sized_variations = filter(lambda x: x.width == 125 and x.height == 125,
                                  self.variation_set.all())
        localized_variation = next((v for v in sized_variations if v.locale == locale), None)

        # Fallback to en-US if no localized variations are found.
        if localized_variation:
            kwargs['preview_img'] = localized_variation.image.url
        elif locale != 'en-us':
            fallback_variation = next((v for v in sized_variations if v.locale == 'en-us'), None)
            if fallback_variation:
                kwargs['preview_img'] = fallback_variation.image.url

        return Markup(render_to_string(self.preview_template, kwargs))

    class Meta:
        abstract = True


class ImageBanner(CachingMixin, ImageBannerBase):
    """Banner displayed as an image link."""
    objects = CachingManager()

    def generate_banner_code(self, variation):
        return render_to_string('banners/banner_code/image_banner.html', {
            'variation': variation
        })

    def get_customize_url(self):
        return reverse('banners.generator.image_banner.customize', kwargs={'pk': self.pk})

    @staticmethod
    def get_variation_class():
        return ImageBannerVariation


class ImageVariation(BannerVariation):
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

    image = models.ImageField(upload_to=_filename, max_length=255, storage=OverwritingStorage(),
                              width_field='width', height_field='height')
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

    @property
    def size(self):
        return '{width} &times; {height}'.format(width=self.width, height=self.height)

    def get_media_subdirectory(self):
        """
        Return the name to use for the subdirectory to store variations
        in, under MEDIA_ROOT.
        """
        raise NotImplementedError()

    def __unicode__(self):
        return u'{size} {color} {locale}'.format(size=self.size, color=self.color,
                                                 locale=self.locale)


class ImageBannerVariation(CachingMixin, ImageVariation):
    banner = models.ForeignKey(ImageBanner, related_name='variation_set')

    objects = CachingManager()

    def get_media_subdirectory(self):
        return 'uploads/image_banners'


class TextBanner(CachingMixin, Banner):
    """Banner displayed as a string of text with a link."""
    objects = CachingManager()

    def generate_banner_code(self, variation):
        return u'<a href="{{href}}">{text}</a>'.format(text=variation.text)

    def get_customize_url(self):
        return reverse('banners.generator.text_banner.customize', kwargs={'pk': self.pk})

    def preview_html(self, href, **kwargs):
        kwargs['href'] = href
        kwargs['banner'] = self

        # Fetch localized variation.
        locale = translation.get_language()
        try:
            kwargs['preview_text'] = self.variation_set.get(locale=locale).text
        except TextBannerVariation.DoesNotExist:
            pass

        # Fallback to en-US if necessary.
        if 'preview_text' not in kwargs and locale != 'en-us':
            try:
                kwargs['preview_text'] = self.variation_set.get(locale='en-us').text
            except TextBannerVariation.DoesNotExist:
                pass

        return Markup(render_to_string('banners/previews/text_banner.html', kwargs))

    @staticmethod
    def get_variation_class():
        return TextBannerVariation


class TextBannerVariation(CachingMixin, BannerVariation):
    """Localized variation of a text banner."""
    banner = models.ForeignKey(TextBanner, related_name='variation_set')
    text = models.TextField()
    locale = LocaleField()

    objects = CachingManager()

    def __unicode__(self):
        return locale_to_native(self.locale)


class FirefoxUpgradeBanner(CachingMixin, ImageBannerBase):
    """
    Image banner that shows a different image depending on whether the
    viewer has an up-to-date version of Firefox or not.
    """
    preview_template = 'banners/previews/upgrade_banner.html'

    objects = CachingManager()

    def generate_banner_code(self, variation):
        return render_to_string('banners/banner_code/firefox_upgrade_banner.html', {
            'variation': variation
        })

    def get_customize_url(self):
        return reverse('banners.generator.firefox_upgrade_banner.customize',
                       kwargs={'pk': self.pk})

    @staticmethod
    def get_variation_class():
        return FirefoxUpgradeBannerVariation


class FirefoxUpgradeBannerVariation(CachingMixin, ImageVariation):
    banner = models.ForeignKey(FirefoxUpgradeBanner, related_name='variation_set')

    objects = CachingManager()

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
        return absolutify(media('uploads/upgrade/{pk}'.format(pk=self.pk)))
