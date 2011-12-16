from django.conf import settings

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_

from shared.tests import TestCase


@patch.object(settings, 'LANGUAGES', {'fy-nl': 'Frysk'})
class L10nTest(TestCase):
    def test_basic(self):
        """Test that LOCALE and LANGUAGE are correct."""
        with self.activate('fy-NL'):
            response = self.client.get(reverse('home'))

        eq_(response.context['LOCALE'], 'fy-nl')
        eq_(response.context['LANGUAGE'], 'Frysk')
