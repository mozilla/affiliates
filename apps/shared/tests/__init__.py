from smtplib import SMTPException

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.management import call_command
from django.db.models import loading

from test_utils import TestCase


class BrokenSMTPBackend(BaseEmailBackend):
    """Simulates an email backend that throws errors."""
    def send_messages(self, email_messages):
        raise SMTPException('Dummy')


def model_ids(models):
    """Generates a list of model ids from a list of model objects."""
    return [m.pk for m in models]


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
