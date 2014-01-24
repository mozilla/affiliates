from django.conf import settings
from django.http import HttpResponse

import basket
from funfactory.urlresolvers import reverse
from mock import ANY, patch
from nose.tools import eq_, ok_

from affiliates.shared.tests import TestCase
from affiliates.users.tests import UserFactory


class TestHome(TestCase):
    fixtures = ['registered_users']

    def test_redirect_logged_in(self):
        self.client.login(username='mkelly@mozilla.com', password='asdfasdf')
        with self.activate('en-US'):
            response = self.client.get(reverse('home'))
        eq_(response.status_code, 302)

    @patch('affiliates.shared.views.browserid_home')
    @patch.object(settings, 'BROWSERID_LOCALES', ['en-us', 'es'])
    def test_browserid_locales(self, browserid_home):
        """Test that users in locales listed in BROWSERID_LOCALES see the
        browserid view while others don't.
        """
        browserid_home.return_value = HttpResponse()

        with self.activate('fr'):
            self.client.get(reverse('home'))
        ok_(not browserid_home.called, 'browserid_home called for '
            'non-browserid locale')

        browserid_home.reset_mock()
        with self.activate('en-US'):
            self.client.get(reverse('home'))
        ok_(browserid_home.called, 'browserid_home not called for browserid '
            'locale')

        # Test non-en-US locale (en-US was previously a special case).
        browserid_home.reset_mock()
        with self.activate('es'):
            self.client.get(reverse('home'))
        ok_(browserid_home.called, 'browserid_home not called for browserid '
            'locale')


class ErrorPageTests(TestCase):
    def _get(self, url):
        with self.activate('en-US'):
            return self.client.get(reverse(url))

    def test_404(self):
        response = self._get('404')
        eq_(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_facebook_404(self):
        response = self._get('facebook.404')
        eq_(response.status_code, 404)
        self.assertTemplateUsed(response, 'facebook/error.html')

    def test_500(self):
        response = self._get('500')
        eq_(response.status_code, 500)
        self.assertTemplateUsed(response, '500.html')

    def test_facebook_500(self):
        response = self._get('facebook.500')
        eq_(response.status_code, 500)
        self.assertTemplateUsed(response, 'facebook/error.html')


@patch.object(basket, 'subscribe')
@patch.object(settings, 'BASKET_NEWSLETTER', 'test-list')
class NewsletterSubscribeTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.browserid_login(self.user.email)

    def subscribe(self, **kwargs):
        with self.activate('en-US'):
            return self.client.post(reverse('shared.newsletter.subscribe'),
                                    kwargs)

    def test_invalid_form_returns_success(self, subscribe):
        """
        Test that even if the form is invalid, return a 200 OK. This will go
        away once we have strings translated for an error message.
        """
        response = self.subscribe(email='')
        eq_(response.status_code, 200)
        ok_(not subscribe.called)

    def test_valid_form_call_basket(self, subscribe):
        """If the form is valid, call basket with the proper arguments."""
        response = self.subscribe(email='test@example.com')
        eq_(response.status_code, 200)
        subscribe.assert_called_with('test@example.com', 'test-list',
                                     source_url=ANY)

    @patch('affiliates.shared.views.log')
    def test_basket_error_log(self, log, subscribe):
        """If basket throws an exception, log it and return a 200 OK."""
        subscribe.side_effect = basket.BasketException
        response = self.subscribe(email='test@example.com')
        eq_(response.status_code, 200)
        ok_(log.error.called)
