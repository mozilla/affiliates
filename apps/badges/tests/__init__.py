from django.conf import settings
from django.core.management import call_command
from django.db.models import loading
from django.test.client import Client

from funfactory.urlresolvers import split_path
from test_utils import TestCase


class LocalizingClient(Client):

    """
    Client which prepends a locale so test requests can get through
    LocaleURLMiddleware without resulting in a locale-prefix-adding 301.

    Otherwise, we'd have to hard-code locales into our tests everywhere or
    {mock out reverse() and make LocaleURLMiddleware not fire}.
    """
    def request(self, **request):
        """Make a request, but prepend a locale if there isn't one already."""
        # Fall back to defaults as in the superclass's implementation:
        path = request.get('PATH_INFO', self.defaults.get('PATH_INFO', '/'))
        locale, shortened = split_path(path)
        if not locale:
            request['PATH_INFO'] = '/%s/%s' % (settings.LANGUAGE_CODE,
                                               shortened)
        return super(LocalizingClient, self).request(**request)


class ModelsTestCase(TestCase):
    """
    Does some pre-setup and post-teardown work to create tables for any
    of your test models.

    Simply subclass this and set self.apps to a tuple of *additional*
    installed apps. These will be added *after* the ones in
    settings.INSTALLED_APPS.

    Based on http://stackoverflow.com/questions/502916#1827272
    """
    apps = []

    def _pre_setup(self):
        # Add the models to the db.
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        for app in self.apps:
            settings.INSTALLED_APPS.append(app)
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, verbosity=0)
        # Call the original method that does the fixtures etc.
        super(ModelsTestCase, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method.
        super(ModelsTestCase, self)._post_teardown()
        # Restore the settings.
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False
