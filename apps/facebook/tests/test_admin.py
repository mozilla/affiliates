import os
from os.path import abspath, dirname

from django.contrib.auth.models import User

from funfactory.urlresolvers import reverse
from nose.tools import eq_

from facebook.models import FacebookBannerLocale
from facebook.tests import FacebookBannerFactory, FacebookBannerLocaleFactory
from shared.tests import TestCase


def path(*a):
    return os.path.join(dirname(abspath(__file__)), *a)


class FacebookBannerAdminTests(TestCase):
    def setUp(self):
        """Create an admin user and log in as them for each test."""
        admin = User.objects.create_user('a@b.com', 'a@b.com', 'asdf1234')
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()

        self.client.login(username='a@b.com', password='asdf1234')

    def test_create_new_banner(self):
        """
        Test if creating a new banner works. Specifically, test if the
        FacebookBannerLocales are created correctly.
        """
        url = reverse('admin:facebook_facebookbanner_add')
        image = open(path('images', 'firefox-small.png'), 'r')
        self.client.post(url, {'name': 'NewBannerTest',
                         'locales': ['en-us', 'fr'], 'image': image})

        locales = (FacebookBannerLocale.objects
                   .filter(banner__name='NewBannerTest'))
        eq_([l.locale for l in locales], ['en-us', 'fr'])

    def test_edit_banner_delete_locales(self):
        """
        Test if removing locales from the locale list deletes their entries
        in the database.
        """
        banner = FacebookBannerFactory.create(name='EditBannerTest')
        FacebookBannerLocaleFactory.create(banner=banner, locale='en-us')
        FacebookBannerLocaleFactory.create(banner=banner, locale='fr')

        locales = FacebookBannerLocale.objects.filter(banner__id=banner.id)
        eq_([l.locale for l in locales], ['en-us', 'fr'])

        url = reverse('admin:facebook_facebookbanner_change', args=(banner.id,))
        self.client.post(url, {'name': 'EditBannerTest',
                         'locales': ['fr']})

        locales = FacebookBannerLocale.objects.filter(banner__id=banner.id)
        eq_([l.locale for l in locales], ['fr'])
