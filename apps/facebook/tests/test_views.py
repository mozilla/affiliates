import json
from datetime import datetime

from django.conf import settings

import basket
from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from facebook.models import (FacebookAccountLink, FacebookBannerInstance,
                             FacebookUser)
from facebook.tests import (create_payload, FacebookAccountLinkFactory,
                            FacebookBannerFactory,
                            FacebookBannerInstanceFactory,
                            FacebookClickStatsFactory, FacebookUserFactory)
from shared.tests import TestCase
from shared.utils import absolutify
from users.tests import UserFactory


@patch.object(FacebookUser.objects, 'update_user_info')
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

    def test_no_signed_request(self, update_user_info):
        """
        If no signed request is provided, the app was loaded outside of the
        Facebook canvas, and we should redirect to the homepage.
        """
        with self.activate('en-US'):
            response = self.load_app(None)
            eq_(response.status_code, 302)
            self.assert_viewname_url(response['Location'], 'home')

    def test_invalid_signed_request(self, update_user_info):
        """If the signed request is invalid, redirect to the homepage."""
        with self.activate('en-US'):
            response = self.load_app(False)
            eq_(response.status_code, 302)
            self.assert_viewname_url(response['Location'], 'home')

    def test_no_authorization(self, update_user_info):
        """
        If the user has yet to authorize the app, ask the user for
        authorization via the oauth_redirect.html template.
        """
        payload = create_payload(user_id=None)
        response = self.load_app(payload)
        self.assertTemplateUsed(response, 'facebook/oauth_redirect.html')

    @patch.object(FacebookUser, 'is_new', False)
    def test_has_authorization(self, update_user_info):
        """
        If the user has authorized the app and isn't new, show the main
        banner view.
        """
        payload = create_payload(user_id=1)
        response = self.load_app(payload)
        self.assertTemplateUsed(response, 'facebook/banner_list.html')

    @patch.object(FacebookUser, 'is_new', True)
    def test_firstrun_page(self, update_user_info):
        """If the user is new, show the firstrun page."""
        payload = create_payload(user_id=1)
        response = self.load_app(payload)
        self.assertTemplateUsed(response, 'facebook/first_run.html')

    @patch('facebook.views.login')
    def test_country_saved(self, login, update_user_info):
        """
        When a user enters the app, their country should be set and
        login should be called with the updated user object so that it will be
        saved to the database.
        """
        user = FacebookUserFactory.create(country='us')
        payload = create_payload(user_id=user.id, country='fr')
        self.load_app(payload)

        eq_(login.called, True)
        eq_(login.call_args[0][1].country, 'fr')


class CreateBannerTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        self.client.fb_login(self.user)

    def banner_create(self, **post_data):
        """Execute banner_create view. kwargs are POST arguments."""
        with self.activate('en-US'):
            return self.client.post(reverse('facebook.banner_create'),
                                    post_data)

    @patch('facebook.views.generate_banner_instance_image.delay')
    def test_use_profile_image(self, delay):
        """
        If the user checked `use_profile_image`, create a banner instance,
        trigger the celery task and return a 202 Accepted.
        """
        banner = FacebookBannerFactory.create()
        response = self.banner_create(banner=banner.id, text='asdf',
                                      next_action='', use_profile_image=True)

        # Asserts that banner instance exists.
        instance = FacebookBannerInstance.objects.get(banner=banner,
                                                      user=self.user)
        delay.assert_called_with(instance.id)

        # Assert response contians the expected links.
        eq_(response.status_code, 202)
        response_data = json.loads(response.content)
        with self.activate('en-US'):
            eq_(response_data['next'],
                absolutify(reverse('facebook.banner_list')))
            eq_(response_data['check_url'],
                reverse('facebook.banners.create_image_check',
                        args=[instance.id]))

    def test_no_profile_image(self):
        """
        If the user did not check `use_profile_image`, create the banner
        instance and return a 201 Created.
        """
        banner = FacebookBannerFactory.create()
        response = self.banner_create(banner=banner.id, text='asdf',
                                      next_action='', use_profile_image=False)
        ok_(FacebookBannerInstance.objects.filter(banner=banner, user=self.user)
            .exists())

        eq_(response.status_code, 201)
        response_data = json.loads(response.content)
        with self.activate('en-US'):
            eq_(response_data['next'],
                absolutify(reverse('facebook.banner_list')))

    def test_save_and_share(self):
        """
        If the user clicks the `Save and Share` button, the `next` link should
        point to the share page for the new banner instance.
        """
        banner = FacebookBannerFactory.create()
        response = self.banner_create(banner=banner.id, text='asdf',
                                      next_action='share',
                                      use_profile_image=False)
        instance = FacebookBannerInstance.objects.get(banner=banner,
                                                      user=self.user)

        response_data = json.loads(response.content)
        with self.activate('en-US'):
            eq_(response_data['next'],
                absolutify(reverse('facebook.banners.share',
                           args=[instance.id])))

    def test_error(self):
        """
        If the form is not valid, return a 400 Bad Request with the error dict
        in JSON.
        """
        response = self.banner_create(next_action='')
        eq_(response.status_code, 400)

        response_data = json.loads(response.content)
        ok_('text' in response_data)
        ok_('banner' in response_data)


class BannerCreateImageCheckTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        self.client.fb_login(self.user)

    def check(self, instance_id):
        with self.activate('en-US'):
            url = reverse('facebook.banners.create_image_check',
                          args=[instance_id])
            return self.client.get(url)

    def test_basic(self):
        instance = FacebookBannerInstanceFactory.create(user=self.user)
        response = self.check(instance.id)
        eq_(json.loads(response.content)['is_processed'], False)

        instance = FacebookBannerInstanceFactory.create(user=self.user,
                                                        processed=True)
        response = self.check(instance.id)
        eq_(json.loads(response.content)['is_processed'], True)


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


@patch.object(basket, 'subscribe')
@patch.object(settings, 'FACEBOOK_MAILING_LIST', 'test-list')
class NewsletterSubscribeTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        self.client.fb_login(self.user)

    def subscribe(self, **kwargs):
        with self.activate('en-US'):
            return self.client.post(reverse('facebook.newsletter.subscribe'),
                                    kwargs)

    def test_invalid_form_returns_success(self, subscribe):
        """
        Test that even if the form is invalid, return a 200 OK. This will go
        away once we have strings translated for an error message.
        """
        response = self.subscribe(country='does.not.exist')
        eq_(response.status_code, 200)
        ok_(not subscribe.called)

    def test_valid_form_call_basket(self, subscribe):
        """If the form is valid, call basket with the proper arguments."""
        response = self.subscribe(email='test@example.com', country='us',
                                  format='text', privacy_policy_agree=True)
        eq_(response.status_code, 200)
        subscribe.assert_called_with('test@example.com', 'test-list',
                                     format='text', country='us')

    @patch('facebook.views.log')
    def test_basket_error_log(self, log, subscribe):
        """If basket throws an exception, log it and return a 200 OK."""
        subscribe.side_effect = basket.BasketException
        response = self.subscribe(email='test@example.com', country='us',
                                  format='text', privacy_policy_agree=True)
        eq_(response.status_code, 200)
        ok_(log.error.called)


@patch.object(settings, 'FACEBOOK_DOWNLOAD_URL', 'http://mozilla.org')
class FollowBannerLinkTests(TestCase):
    def follow_link(self, instance_id):
        with self.activate('en-US'):
            return self.client.get(reverse('facebook.banners.link',
                                   args=[instance_id]))

    def test_instance_does_not_exist(self):
        """
        If the requested banner instance does not exist, return the default
        redirect.
        """
        response = self.follow_link(999)
        self.assert_redirects(response, 'http://mozilla.org')

    @patch('facebook.views.add_click')
    def test_banner_redirect(self, add_click):
        """
        If the requested banner instance exists, return a redirect to the
        parent banner's link.
        """
        instance = FacebookBannerInstanceFactory.create(
            banner__link='http://allizom.org')
        response = self.follow_link(instance.id)
        self.assert_redirects(response, 'http://allizom.org')
        add_click.delay.assert_called_with(unicode(instance.id))
