from django.core.files import File

import requests
from nose.tools import eq_, ok_
from mock import patch
from PIL import Image, ImageChops

from facebook.models import FacebookBannerInstance, FacebookClickStats
from facebook.tasks import add_click, generate_banner_instance_image
from facebook.tests import FacebookBannerInstanceFactory, path
from shared.tests import TestCase


class AddClickTests(TestCase):
    @patch.object(FacebookClickStats.objects, 'get_or_create')
    def test_invalid_id(self, get_or_create):
        """If the given banner id is invalid, do nothing."""
        add_click(999)
        ok_(not get_or_create.called)

    def test_valid_id(self):
        """If the given banner id is valid, increment the click count."""
        banner = FacebookBannerInstanceFactory(total_clicks=0)
        add_click(banner.id)

        banner_instance = FacebookBannerInstance.objects.get(id=banner.id)
        eq_(banner_instance.total_clicks, 1)

        stats = FacebookClickStats.objects.get(banner_instance=banner_instance)
        eq_(stats.clicks, 1)


def image_response(*image_path):
    """Return a mock Requests response with an image as the content."""
    response = requests.Response()
    with open(path(*image_path), 'rb') as image_file:
        response._content = image_file.read()
    return lambda url: response


class GenerateBannerInstanceImageTests(TestCase):
    def generate(self, instance_id):
        return generate_banner_instance_image(instance_id)

    def instance(self, **kwargs):
        return FacebookBannerInstanceFactory.create(**kwargs)

    def test_invalid_id(self):
        """If an invalid id is given, do nothing."""
        self.generate(999)  # No exceptions!

    @patch.object(requests, 'get')
    def test_download_user_image_error(self, get):
        """If there is an error downloading the user's photo, do nothing."""
        get.side_effect = requests.exceptions.RequestException
        instance = self.instance()

        self.generate(instance.id)
        instance = FacebookBannerInstance.objects.get(id=instance.id)
        eq_(bool(instance.custom_image), False)

    @patch.object(requests, 'get', image_response('images', 'fb_picture.jpg'))
    @patch('facebook.tasks.Image')
    def test_invalid_image(self, Image):
        """If PIL throws an exception when opening the images, do nothing."""
        Image.open.side_effect = ValueError
        instance = self.instance()

        eq_(self.generate(instance.id), None)
        instance = FacebookBannerInstance.objects.get(id=instance.id)
        eq_(bool(instance.custom_image), False)

    @patch.object(requests, 'get', image_response('images', 'fb_picture.jpg'))
    def test_banner_generation(self):
        """Test that the image generation creates the expected image."""
        instance = self.instance()
        with open(path('images', 'banner.png')) as banner_image:
            instance.banner.image.save('test.png', File(banner_image))

        self.generate(instance.id)
        instance = FacebookBannerInstance.objects.get(id=instance.id)

        custom_im = Image.open(instance.custom_image)
        reference_im = Image.open(path('images', 'expected_banner.png'))

        # effbot delivers! http://effbot.org/zone/pil-comparing-images.htm
        match = ImageChops.difference(custom_im, reference_im).getbbox() is None
        eq_(match, True)
