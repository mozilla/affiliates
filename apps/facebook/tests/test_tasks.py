import unittest

from django.conf import settings
from django.core import mail
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

    @patch.object(settings, 'FACEBOOK_CLICK_GOAL', 30)
    @patch.object(settings, 'FACEBOOK_CLICK_GOAL_EMAIL', 'admin@example.com')
    def test_admin_email(self):
        """
        If the banner instance has just reached the click goal, email the admin.
        """
        instance = FacebookBannerInstanceFactory.create(total_clicks=29)
        add_click(instance.id)

        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].subject, ('[fb-affiliates-banner] Click Goal '
                                     'Reached!'))
        ok_(unicode(instance.id) in mail.outbox[0].body)
        ok_('admin@example.com' in mail.outbox[0].to)


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

    @patch.object(requests, 'get')
    def test_invalid_id(self, get):
        """If an invalid id is given, do nothing."""
        self.generate(999)  # No exceptions!
        eq_(get.called, False)

    @patch.object(requests, 'get')
    def test_download_user_image_error(self, get):
        """If there is an error downloading the user's photo, do nothing."""
        get.side_effect = requests.exceptions.RequestException
        instance = self.instance()

        self.generate(instance.id)
        instance = FacebookBannerInstance.objects.get(id=instance.id)
        eq_(bool(instance.custom_image), False)
        eq_(instance.processed, False)

    @patch.object(requests, 'get', image_response('images', 'fb_picture.jpg'))
    @patch('facebook.tasks.Image')
    def test_invalid_image(self, Image):
        """If PIL throws an exception when opening the images, do nothing."""
        Image.open.side_effect = ValueError
        instance = self.instance()

        self.generate(instance.id)
        instance = FacebookBannerInstance.objects.get(id=instance.id)
        eq_(bool(instance.custom_image), False)
        eq_(instance.processed, False)

    # Images may differ slightly between machines, so we're skipping this
    # test for now until a better image comparison function can be found.
    @unittest.skip('Skipping test until better image comparison is added.')
    @patch.object(requests, 'get', image_response('images', 'fb_picture.jpg'))
    def test_banner_generation(self):
        """Test that the image generation creates the expected image."""
        instance = self.instance()
        with open(path('images', 'banner.png')) as banner_image:
            instance.banner.image.save('test.png', File(banner_image))

        self.generate(instance.id)
        instance = FacebookBannerInstance.objects.get(id=instance.id)
        eq_(instance.processed, True)

        custom_im = Image.open(instance.custom_image)
        reference_im = Image.open(path('images', 'expected_banner.png'))

        # effbot delivers! http://effbot.org/zone/pil-comparing-images.html
        diff = ImageChops.difference(custom_im, reference_im)
        diff.save(path('images', 'test_banner_generation_diff.png'))
        bbox = diff.getbbox()
        ok_(bbox is None, 'bbox is %s' % (bbox,))

        # Cleanup
        instance.banner.image.delete()
        instance.custom_image.delete()
