from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from facebook.models import FacebookBannerInstance, FacebookUser
from facebook.tests import (create_payload, FacebookBannerFactory,
                            FacebookUserFactory)
from shared.tests import TestCase


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
