from contextlib import contextmanager, nested
from functools import wraps
from smtplib import SMTPException

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.mail.backends.base import BaseEmailBackend
from django.core.management import call_command
from django.db.models import loading
from django.test.client import RequestFactory
from django.utils.translation import get_language

import test_utils
from funfactory.urlresolvers import (get_url_prefix, Prefixer, reverse,
                                     set_url_prefix)
from mock import patch
from nose.tools import eq_, ok_
from tower import activate

from browserid.tests import mock_browserid
from facebook.tests import FacebookAuthClient


class BrokenSMTPBackend(BaseEmailBackend):
    """Simulates an email backend that throws errors."""
    def send_messages(self, email_messages):
        raise SMTPException('Dummy')


def model_ids(models):
    """Generates a list of model ids from a list of model objects."""
    return [m.pk for m in models]


class SessionRequestFactory(RequestFactory):
    """RequestFactory that adds session data to requests."""
    def __init__(self, *args, **kwargs):
        super(SessionRequestFactory, self).__init__(*args, **kwargs)
        self.session_middleware = SessionMiddleware()

    def request(self, *args, **kwargs):
        request = super(SessionRequestFactory, self).request(*args, **kwargs)
        self.session_middleware.process_request(request)
        return request


class TestCase(test_utils.TestCase):
    """Base class for Affiliates test cases."""
    client_class = FacebookAuthClient

    @contextmanager
    def activate(self, locale):
        """Context manager that temporarily activates a locale."""
        old_prefix = get_url_prefix()
        old_locale = get_language()
        rf = test_utils.RequestFactory()
        set_url_prefix(Prefixer(rf.get('/%s/' % (locale,))))
        activate(locale)
        yield
        set_url_prefix(old_prefix)
        activate(old_locale)

    def browserid_login(self, email):
        """Logs the test client in using BrowserID."""
        factory = SessionRequestFactory()
        with self.activate('en-US'):
            request = factory.get(reverse('home'))
        with mock_browserid(email):
            self.client.login(request=request, assertion='asdf')

    def assert_viewname_url(self, url, viewname, locale='en-US'):
        """Compare a viewname's url to a given url."""
        with self.activate(locale):
            view_url = reverse(viewname)

        return ok_(url.endswith(view_url),
                   'URL Match failed: %s != %s' % (url, view_url))

    def assert_redirects(self, response, url, status=302):
        """Assert that the given response redirects to the given url."""
        eq_(response.status_code, status)
        eq_(response['Location'], url)


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


def refresh_model(instance):
    """Retrieves the latest version of a model instance from the DB."""
    return instance.__class__.objects.get(pk=instance.pk)


def patch_settings(**new_settings):
    """
    Syntactic sugar for patching many settings at once.

    TODO: Replace with override_settings in Django 1.4.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            patches = []
            for name, value in new_settings.items():
                patches.append(patch.object(settings, name, value))
            with nested(*patches):
                return f(*args, **kwargs)
        return wrapped
    return decorator
