from django.conf import settings
from django.core import mail

import requests
from nose.tools import eq_, ok_
from mock import patch

from affiliates.facebook.models import FacebookBannerInstance, FacebookClickStats
from affiliates.facebook.tasks import add_click, generate_banner_instance_image
from affiliates.facebook.tests import FacebookBannerInstanceFactory, path
from affiliates.shared.tests import TestCase


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

    @patch('facebook.tasks.CLICK_MILESTONES', {5: 'test'})
    def test_click_milestones(self):
        """If the new click count is a click milestone, send a notification."""
        instance = FacebookBannerInstanceFactory.create(total_clicks=3)
        add_click(instance.id)
        eq_(len(instance.user.appnotification_set.all()), 0)

        add_click(instance.id)
        eq_(len(instance.user.appnotification_set.all()), 1)
        notification = instance.user.appnotification_set.all()[0]
        eq_(notification.message, 'test')
        eq_(notification.format_argument, '5')


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
