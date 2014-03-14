from contextlib import contextmanager
from datetime import datetime
from urlparse import urlsplit, urlunsplit

from django.test import TestCase as DjangoTestCase
from django.utils.translation import get_language
from django.utils import timezone

import test_utils
from factory import DjangoModelFactory, Sequence, SubFactory
from funfactory.urlresolvers import get_url_prefix, Prefixer, set_url_prefix
from mock import patch
from nose.tools import eq_
from tower import activate

from affiliates.base import models
from affiliates.facebook.tests import FacebookAuthClient
from affiliates.users.tests import UserFactory


class TestCase(DjangoTestCase):
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

    def assertRedirectsNoFollow(self, response, expected_url, status=302):
        """
        Assert that the given response redirects to the given url
        without following the redirect.
        """
        eq_(response.status_code, status)

        # If expected_url has no scheme or netloc, steal them from the
        # redirect's location so we can compare just the paths.
        # Adapted from assertRedirects.
        e_scheme, e_netloc, e_path, e_query, e_fragment = urlsplit(expected_url)
        if not (e_scheme or e_netloc):
            scheme, netloc, path, query, fragment = urlsplit(response['Location'])
            expected_url = urlunsplit((scheme, netloc, e_path, e_query, e_fragment))

        eq_(response['Location'], expected_url)

    def create_patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        obj = patcher.start()
        self.addCleanup(patcher.stop)
        return obj

    def shortDescription(self):
        # Stop nose using the test docstring and instead the test method
        # name.
        pass


def refresh_model(instance):
    """Retrieves the latest version of a model instance from the DB."""
    return instance.__class__.objects.get(pk=instance.pk)


def patch_super(obj, attr):
    """Patch the given attribute on the object's superclass."""
    return patch.object(obj.__class__.__bases__[0], attr)


def aware_datetime(*args, **kwargs):
    dt = datetime(*args, **kwargs)
    return timezone.make_aware(dt, timezone.utc)


def aware_date(*args, **kwargs):
    return aware_datetime(*args, **kwargs).date()


class NewsItemFactory(DjangoModelFactory):
    FACTORY_FOR = models.NewsItem

    author = SubFactory(UserFactory)
    title = Sequence(lambda n: 'Test Title {0}'.format(n))
    html = Sequence(lambda n: '<p>Acting {0}</p>'.format(n))


class NewsItemTranslationFactory(DjangoModelFactory):
    FACTORY_FOR = models.NewsItemTranslation

    newsitem = SubFactory(NewsItemFactory)
    locale = 'de'
    title = Sequence(lambda n: 'Test Titel {0}'.format(n))
    html = Sequence(lambda n: '<p>Schauspielkunst {0}</p>'.format(n))
