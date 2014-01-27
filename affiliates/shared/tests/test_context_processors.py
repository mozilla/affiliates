from django.conf import settings

from mock import Mock, patch
from nose.tools import eq_

from affiliates.shared.context_processors import l10n
from affiliates.shared.tests import TestCase


@patch.object(settings, 'LANGUAGES', {'fy-nl': 'Frysk'})
class L10nTest(TestCase):
    def test_basic(self):
        """Test that LOCALE and LANGUAGE are correct."""
        request = Mock()
        with self.activate('fy-NL'):
            ctx = l10n(request)
            eq_(ctx['LOCALE'], 'fy-nl')
            eq_(ctx['LANGUAGE'], 'Frysk')
