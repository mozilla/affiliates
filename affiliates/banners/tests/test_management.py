from collections import defaultdict

from django.core.management import CommandError
from django.test.utils import override_settings

from mock import ANY, mock_open, patch

from affiliates.banners.management.commands import generate_media_htaccess
from affiliates.base.tests import TestCase


class GenerateMediaHtaccessTests(TestCase):
    def setUp(self):
        self.command = generate_media_htaccess.Command()

        product_details_patch = patch.object(generate_media_htaccess, 'product_details')
        self.addCleanup(product_details_patch.stop)
        self.mock_product_details = product_details_patch.start()

    def test_version_unavailable(self):
        """
        If the Firefox version number is not available, raise a
        CommandError.
        """
        self.mock_product_details.firefox_versions = defaultdict(lambda: None)
        with self.assertRaises(CommandError):
            self.command.handle()

    def test_invalid_version(self):
        """If the version string is invalid, raise a CommandError."""
        self.mock_product_details.firefox_versions = {'LATEST_FIREFOX_VERSION': '3gabe'}
        with self.assertRaises(CommandError):
            self.command.handle()

    @override_settings(MEDIA_ROOT='/media')
    def test_basic(self):
        _open = mock_open()

        # So much mocking.
        self.mock_product_details.firefox_versions = {'LATEST_FIREFOX_VERSION': '12.0'}
        with patch.object(generate_media_htaccess, 'open', _open, create=True):
            with patch.object(generate_media_htaccess, 'render_to_string') as render_to_string:
                render_to_string.return_value = 'rendered_htaccess'
                self.command.handle()

        # Rendered with correct regex and wrote correct output to
        # correct file.
        render_to_string.assert_called_with('banners/media.htaccess', {
            'version_regex': '12|13|14|15',
            'upgrade_banner_variations': ANY
        })
        _open.assert_called_with('/media/.htaccess', 'w')
        _open.return_value.write.assert_called_with('rendered_htaccess')
