from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User

from mock import patch
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import Badge, BadgeInstance, ClickStats, Subcategory


class FakeDatetime(datetime):
    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)


class SubcategoryTests(TestCase):
    fixtures = ['subcategories', 'badge_previews']

    def test_in_locale(self):
        """
        Test that ``in_locale`` returns all subcategories with badges available
        in the given locale.
        """
        results = Subcategory.objects.in_locale('en-us')
        eq_(len(results), 2)

        results = Subcategory.objects.in_locale('es')
        eq_(len(results), 1)

    def test_preview_img_url(self):
        """
        Test that ``preview_img_url`` pulls a badge preview from within the
        subcategory.
        """
        subcategory = Subcategory.objects.get(pk=21)
        preview = subcategory.preview_img_url('en-us')

        # Previews in subcategory 21 have 'cat1' in their path
        ok_('cat1' in preview,
            u'Preview not from correct subcategory: %s' % preview)


class BadgeTests(TestCase):
    fixtures = ['badge_previews']

    @patch.object(settings, 'DEFAULT_BADGE_PREVIEW', 'default')
    def test_preview_img_url_default(self):
        """
        Test that ``preview_img_url`` returns the default preview if a locale
        preview does not exist.
        """
        badge = Badge.objects.get(pk=2)
        preview = badge.preview_img_url('es')
        eq_(preview, 'default')

    def test_preview_img_url_locale(self):
        """Test that ``preview_img_url`` returns the correct locale preview."""
        badge = Badge.objects.get(pk=2)
        preview = badge.preview_img_url('de')
        ok_(preview.endswith('path/to/cat2/de/image.png'),
            u'Incorrect preview image path.')


class BadgeInstanceTests(TestCase):
    fixtures = ['badge_instance']

    def setUp(self):
        self.badge_instance = BadgeInstance.objects.get(pk=2)

    def test_for_user_by_category(self):
        user = User.objects.get(pk=5)
        categories = BadgeInstance.objects.for_user_by_category(user)
        expect = {'Firefox': [self.badge_instance]}
        eq_(categories, expect)


class ClickStatsTests(TestCase):
    fixtures = ['badge_instance']

    def test_total_for_user_basic(self):
        user = User.objects.get(id=6)
        eq_(ClickStats.objects.total_for_user(user), 23)

    def test_total_for_user_period_basic(self):
        user = User.objects.get(id=6)
        eq_(ClickStats.objects.total_for_user_period(user, 7, 2011), 12)

    def test_average_for_period_basic(self):
        eq_(ClickStats.objects.average_for_period(7, 2011), 6)
        eq_(ClickStats.objects.average_for_period(8, 2011), 11)
