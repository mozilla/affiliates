from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User

from mock import patch
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import Badge, BadgeInstance, ClickStats, Subcategory
from badges.tests import ClickStatsFactory, BadgeInstanceFactory
from shared.tests import refresh_model


class FakeDatetime(datetime):
    def __new__(cls, *args, **kwargs):
        return datetime.__new__(datetime, *args, **kwargs)


class SubcategoryTests(TestCase):
    fixtures = ['subcategories', 'badge_previews']

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

    def _preview(self, pk, locale):
        return Badge.objects.get(pk=pk).preview_img_url(locale)

    @patch.object(settings, 'LANGUAGE_CODE', 'de')
    @patch.object(settings, 'DEFAULT_BADGE_PREVIEW', 'default')
    def test_preview_img_url_fallbacks(self):
        """
        Test that ``preview_img_url`` falls back to the proper banner images.
        """
        # Test for preview that matches requested locale
        ok_(self._preview(3, 'es').endswith('es/image.png'))

        # Test for preview in app default locale
        ok_(self._preview(2, 'es').endswith('de/image.png'))

        # Test for preview in first available locale
        ok_(self._preview(1, 'es').endswith('en-us/image.png'))

        # Test for default when no previews are found
        eq_(self._preview(4, 'es'), 'default')


    def test_preview_img_url_locale(self):
        """Test that ``preview_img_url`` returns the correct locale preview."""
        preview = self._preview(2, 'de')
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

    def test_add_click_basic(self):
        """Test that add_click increments the correct clickstats object."""
        cs = ClickStatsFactory(clicks=4, datetime=datetime(2012, 4, 1))
        cs.badge_instance.add_click(2012, 4)
        cs = refresh_model(cs)
        eq_(cs.clicks, 5)

    def test_add_click_normalized(self):
        """Test that add_click increments the normalized click count."""
        bi = BadgeInstanceFactory(clicks=4)
        bi.add_click(2012, 4)
        bi = refresh_model(bi)
        eq_(bi.clicks, 5)


class ClickStatsTests(TestCase):
    fixtures = ['badge_instance']

    def test_total(self):
        eq_(ClickStats.objects.total(), 24)

    def test_total_for_badge(self):
        badge = Badge.objects.get(id=2)
        eq_(ClickStats.objects.total_for_badge(badge), 23)

    def test_total_for_user_basic(self):
        user = User.objects.get(id=6)
        eq_(ClickStats.objects.total_for_user(user), 23)

    def test_total_for_user_period_basic(self):
        user = User.objects.get(id=6)
        eq_(ClickStats.objects.total_for_user_period(user, 7, 2011), 12)

    def test_average_for_period_basic(self):
        eq_(ClickStats.objects.average_for_period(7, 2011), 6)
        eq_(ClickStats.objects.average_for_period(8, 2011), 11)
