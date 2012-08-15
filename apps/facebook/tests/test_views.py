from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from facebook.models import (FacebookAccountLink, FacebookBannerInstance,
                             FacebookUser)
from facebook.tests import (create_payload, FacebookAccountLinkFactory,
                            FacebookBannerFactory, FacebookUserFactory)
from shared.tests import TestCase
from users.tests import UserFactory


class LoadAppTests(TestCase):
    def load_app(self, payload):
        """
        Runs the load_app view. If payload is None, it will not be
        passed to the view. If it is False, it will fail to be decoded.
        Otherwise, it will be used as the payload.
        """
        post_data = {}
        if payload is not None:
            post_data['signed_request'] = 'signed_request'

        with patch('facebook.views.decode_signed_request') as decode:
            if payload:
                decode.return_value = payload
            else:
                decode.return_value = None

            return self.client.post(reverse('facebook.load_app'), post_data)

    def test_no_signed_request(self):
        """
        If no signed request is provided, the app was loaded outside of the
        Facebook canvas, and we should redirect to the homepage.
        """
        with self.activate('en-US'):
            response = self.load_app(None)
            eq_(response.status_code, 302)
            self.assert_viewname_url(response['Location'], 'home')

    def test_invalid_signed_request(self):
        """If the signed request is invalid, redirect to the homepage."""
        with self.activate('en-US'):
            response = self.load_app(False)
            eq_(response.status_code, 302)
            self.assert_viewname_url(response['Location'], 'home')

    def test_no_authorization(self):
        """
        If the user has yet to authorize the app, ask the user for
        authorization via the oauth_redirect.html template.
        """
        payload = create_payload(user_id=None)
        response = self.load_app(payload)
        self.assertTemplateUsed(response, 'facebook/oauth_redirect.html')

    @patch.object(FacebookUser, 'is_new', False)
    def test_has_authorization(self):
        """
        If the user has authorized the app and isn't new, show the main
        banner view.
        """
        payload = create_payload(user_id=1)
        response = self.load_app(payload)
        self.assertTemplateUsed(response, 'facebook/banner_list.html')

    @patch.object(FacebookUser, 'is_new', True)
    def test_firstrun_page(self):
        """If the user is new, show the firstrun page."""
        payload = create_payload(user_id=1)
        response = self.load_app(payload)
        self.assertTemplateUsed(response, 'facebook/first_run.html')


class CreateBannerTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        self.client.fb_login(self.user)

    def create_banner(self, **post_data):
        """Execute create_banner view. kwargs are POST arguments."""
        with self.activate('en-US'):
            return self.client.post(reverse('facebook.create_banner'),
                                    post_data)

    def test_invalid_form(self):
        """If the form is invalid, redisplay it."""
        response = self.create_banner(banner='asdf')
        self.assertTemplateUsed(response, 'facebook/create_banner.html')

    def test_valid_form(self):
        """
        If the form is valid, create a new banner instance and show the banner
        list.
        """
        banner = FacebookBannerFactory.create()
        response = self.create_banner(banner=banner.id, text='asdf')

        ok_(FacebookBannerInstance.objects.filter(banner=banner, text='asdf')
            .exists())
        self.assertTemplateUsed(response, 'facebook/banner_list.html')


class LinkAccountsTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        with self.activate('en-US'):
            self.url = reverse('facebook.link_accounts')

    def test_not_logged_in(self):
        """If not logged in, return a 403 Forbidden."""
        response = self.client.post(self.url)
        eq_(response.status_code, 403)

    @patch.object(FacebookAccountLink.objects, 'create_link')
    def test_link_failure(self, create_link):
        """If creating a link fails, still return a 200 OK."""
        create_link.return_value = None
        self.client.fb_login(self.user)
        UserFactory.create(email='a@example.com')

        response = self.client.post(self.url,
                                    {'affiliates_email': 'a@example.com'})
        eq_(response.status_code, 200)

    @patch.object(FacebookAccountLink.objects, 'send_activation_email')
    @patch.object(FacebookAccountLink.objects, 'create_link')
    def test_link_success(self, create_link, send_activation_email):
        """
        If creating a link succeeds, send an activation email and return a 200
        OK.
        """
        link = FacebookAccountLinkFactory.create()
        create_link.return_value = link
        self.client.fb_login(self.user)
        UserFactory.create(email='a@example.com')

        response = self.client.post(self.url,
                                    {'affiliates_email': 'a@example.com'})
        eq_(response.status_code, 200)
        ok_(send_activation_email.called)
        eq_(send_activation_email.call_args[0][1], link)
