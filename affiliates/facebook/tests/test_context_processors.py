from django.conf import settings
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_, ok_

from affiliates.facebook.context_processors import app_context
from affiliates.facebook.models import AnonymousFacebookUser
from affiliates.facebook.tests import (AppNotificationFactory, FacebookUserFactory,
                            FacebookAccountLinkFactory)
from affiliates.facebook.utils import activate_locale
from affiliates.shared.tests import TestCase


class AppContextTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('facebook.context_processors.in_facebook_app')
    def _app_context(self, in_facebook_app, path='/', user=None, in_app=True,
                     locale='en-US'):
        in_facebook_app.return_value = in_app
        request = self.factory.get(path)
        request.user = user
        activate_locale(request, locale)
        if request.user is None:
            request.user = AnonymousFacebookUser()

        return app_context(request)

    def test_not_in_facebook_app(self):
        """If the request is not to the Facebook app, return an empty dict."""
        eq_(self._app_context(in_app=False), {})

    def test_account_link_form(self):
        """
        If the user doesn't have a linked account, the account_link_form should
        be included in the context.
        """
        unlinked_account = FacebookUserFactory.create()
        ok_('account_link_form' in self._app_context(user=unlinked_account))

        account_link = FacebookAccountLinkFactory.create(is_active=True)
        linked_account = account_link.facebook_user
        ok_('account_link_form' not in self._app_context(user=linked_account))

    @patch('facebook.context_processors.NewsletterSubscriptionForm')
    def test_newsletter_form(self, NewsletterSubscriptionForm):
        """If the user is logged in, include the newsletter_form."""
        user = FacebookUserFactory()
        ok_('newsletter_form' in self._app_context(user=user, locale='en-US'))
        NewsletterSubscriptionForm.assert_called_with(user,
                                                      auto_id='newsletter_%s')

    @patch.object(settings, 'FACEBOOK_LOCALES', ['en-US', 'en-AU', 'fr', 'de'])
    def test_newsletter_en_only(self):
        """Only show the newsletter to English locales."""
        user = FacebookUserFactory()
        ok_('newsletter_form' in self._app_context(user=user, locale='en-US'))
        ok_('newsletter_form' in self._app_context(user=user, locale='en-AU'))
        ok_(not 'newsletter_form' in self._app_context(user=user, locale='fr'))
        ok_(not 'newsletter_form' in self._app_context(user=user, locale='de'))

    def test_app_notifications(self):
        """If the user is logged in, include all of their app notifications."""
        user = FacebookUserFactory.create()
        notes = [AppNotificationFactory.create(user=user) for x in range(2)]
        eq_(list(self._app_context(user=user)['app_notifications']), notes)
