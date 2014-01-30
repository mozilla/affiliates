import hashlib
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string

from mptt.models import MPTTModel, TreeForeignKey

from affiliates.banners import COLOR_CHOICES
from affiliates.links.models import Link
from affiliates.shared.models import LocaleField


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

    def create_link(self, user, *args, **kwargs):
        """
        Create a Link based off of this banner. Extra arguments are
        passed on to generate_banner_code.
        """
        html = self.generate_banner_code(*args, **kwargs)
        return Link(user=user, destination=self.destination, html=html)


class ImageBanner(Banner):
    """Banner displayed as an image link."""
    def generate_banner_code(self, variation):
        return render_to_string('banners/banner_code/image_banner.html', {
            'href': self.destination,
            'variation': variation
        })


class ImageBannerVariation(models.Model):
    """
    Variation of an image banner that a user can choose to use for their
    link.
    """
    banner = models.ForeignKey(ImageBanner)
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
        return os.path.join('uploads/banners', props_hash + extension)

    image = models.ImageField(upload_to=_filename, max_length=255)


class TextBanner(Banner):
    """
    Banner displayed as a string of text with a link.

    Text should use Python format syntax to include the link. For
    example:

    > Value privacy? <a href="{href}">Download Firefox!</a>
    """
    text = models.TextField()

    def generate_banner_code(self):
        return self.text.format(href=self.destination)
