from os import path

from django.conf import settings
from django.core.management import call_command

from mock import patch
from nose.tools import ok_

from shared.tests import TestCase


class BannersHtaccessTests(TestCase):
    HTACCESS_LOCATION = path.join(settings.MEDIA_ROOT, '.htaccess')

    @patch('os.remove')
    @patch.object(settings, 'BANNERS_HASH', [])
    def test_no_hashes_delete(self, remove):
        """If there are no hashes in BANNERS_HASH, delete .htaccess."""
        call_command('banners_htaccess')
        remove.assert_called_with(self.HTACCESS_LOCATION)

    @patch('os.remove')
    @patch.object(settings, 'BANNERS_HASH', [])
    def test_no_hashes_delete_exception(self, remove):
        """
        If there are no hashes in BANNERS_HASH and .htaccess does not exist,
        the command should exit successfully.
        """
        remove.side_effect = OSError
        call_command('banners_htaccess')  # Nothing should be raised.
        ok_(remove.called)
