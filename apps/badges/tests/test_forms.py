import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from mock import patch
from nose.tools import eq_
from test_utils import TestCase

from badges.forms import BadgeLocaleAdminForm
from badges.models import Badge


TEST_LANGUAGES = {'en-us': 'English (US)', 'de': 'Deutsch'}


class TestForm(BadgeLocaleAdminForm):
    class Meta:
        model = Badge


@patch.object(settings, 'LANGUAGES', TEST_LANGUAGES)
class BadgeLocaleAdminFormTests(TestCase):
    fixtures = ['subcategories']

    def _form(self, **kwargs):
        """Create form with default values."""
        defaults = {
            'name': 'Test Badge',
            'subcategory': 11,
            'href': 'mozilla.org',
            'locales': ['en-us']
        }
        defaults.update(kwargs)

        image_filename = os.path.join(os.path.dirname(__file__), "test.png")
        image_data = open(image_filename, 'rb').read()
        files = {
            'preview_img': SimpleUploadedFile('test.png', image_data)
        }

        return TestForm(defaults, files)

    def test_new_badge(self):
        """Test that creating a new badge works correctly."""
        form = self._form()
        badge = form.save()

        eq_('Test Badge', badge.name)
        eq_(['en-us'], [bl.locale for bl in badge.badgelocale_set.all()])
