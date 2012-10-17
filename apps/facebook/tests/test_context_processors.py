from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_, ok_

from facebook.context_processors import app_context
from facebook.models import AnonymousFacebookUser
from facebook.tests import (AppNotificationFactory, FacebookUserFactory,
                            FacebookAccountLinkFactory)
from shared.tests import TestCase


class AppContextTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('facebook.context_processors.in_facebook_app')
    def _app_context(self, in_facebook_app, path='/', user=None, in_app=True):
        in_facebook_app.return_value = in_app
        request = self.factory.get(path)
        request.user = user
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
        ok_('newsletter_form' in self._app_context(user=user))
        NewsletterSubscriptionForm.assert_called_with(user,
                                                      auto_id='newsletter_%s')

    def test_app_notifications(self):
        """If the user is logged in, include all of their app notifications."""
        user = FacebookUserFactory.create()
        notes = [AppNotificationFactory.create(user=user) for x in range(2)]
        eq_(list(self._app_context(user=user)['app_notifications']), notes)
