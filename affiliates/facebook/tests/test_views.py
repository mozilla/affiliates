import json

from django.conf import settings
from django.http import HttpResponse
from django.test.client import RequestFactory

import basket
from funfactory.urlresolvers import reverse
from mock import ANY, patch
from nose.tools import eq_, ok_

from affiliates.facebook import views
from affiliates.facebook.models import (FacebookAccountLink, FacebookBannerInstance,
                             FacebookUser)
from affiliates.facebook.tests import (create_payload, FACEBOOK_USER_AGENT,
                            FacebookAccountLinkFactory,
                            FacebookBannerInstanceFactory,
                            FacebookBannerLocaleFactory, FacebookUserFactory)
from affiliates.facebook.views import SAFARI_WORKAROUND_KEY
from affiliates.shared.tests import TestCase
from affiliates.shared.utils import absolutify
from affiliates.users.tests import UserFactory


@patch.object(FacebookUser.objects, 'update_user_info')
class LoadAppTests(TestCase):
    def load_app(self, payload, **extra):
        """
        Runs the load_app view. If payload is None, it will not be
        passed to the view. If it is False, it will fail to be decoded.
        Otherwise, it will be used as the payload.
        """
        post_data = {}
        if payload is not None:
            post_data['signed_request'] = 'signed_request'

        with patch('affiliates.facebook.views.decode_signed_request') as decode:
            if payload:
                decode.return_value = payload
            else:
                decode.return_value = None

            return self.client.post(reverse('facebook.load_app'), post_data,
                                    **extra)

    def test_no_signed_request(self, update_user_info):
        """
        If no signed request is provided, the app was loaded outside of the
        Facebook canvas, and we should redirect to the homepage.
        """
        with self.activate('en-US'):
            response = self.load_app(None)
            eq_(response.status_code, 302)
            self.assert_viewname_url(response['Location'], 'base.landing')

    def test_invalid_signed_request(self, update_user_info):
        """If the signed request is invalid, redirect to the homepage."""
        with self.activate('en-US'):
            response = self.load_app(False)
            eq_(response.status_code, 302)
            self.assert_viewname_url(response['Location'], 'base.landing')

    @patch('affiliates.facebook.views.fb_redirect')
    def test_safari_workaround(self, fb_redirect, update_user_info):
        """
        If the user is using Safari and hasn't gone through the workaround yet,
        send them to the workaround page.
        """
        fb_redirect.return_value = HttpResponse()
        payload = create_payload(user_id=1)
        self.load_app(payload, HTTP_USER_AGENT='Safari/5.04')
        ok_(fb_redirect.called)
        self.assert_viewname_url(fb_redirect.call_args[0][1],
                                 'facebook.safari_workaround')

    @patch('affiliates.facebook.views.fb_redirect')
    def test_no_safari_workaround(self, fb_redirect, update_user_info):
        """
        If the user is not using Safari, do not redirect to the workaround.
        """
        with self.activate('en-US'):
            workaround_url = absolutify(reverse('facebook.safari_workaround'))

        fb_redirect.return_value = HttpResponse('blah')
        payload = create_payload(user_id=1)
        response = self.load_app(payload,
                                 HTTP_USER_AGENT='Safari/5.04 Chrome/7.5')

        eq_(response, fb_redirect.return_value)
        ok_(fb_redirect.call_args[0][1] != workaround_url)

    @patch('affiliates.facebook.views.fb_redirect')
    def test_safari_workaround_done(self, fb_redirect, update_user_info):
        """
        If the user is using Safari and hasthe workaround cookie, do not send
        them to the workaround page.
        """
        with self.activate('en-US'):
            workaround_url = absolutify(reverse('facebook.safari_workaround'))

        fb_redirect.return_value = HttpResponse('blah')
        payload = create_payload(user_id=1)
        self.client.cookies[SAFARI_WORKAROUND_KEY] = '1'
        response = self.load_app(payload, HTTP_USER_AGENT='Safari/5.04')
        del self.client.cookies[SAFARI_WORKAROUND_KEY]

        # Ensure that the redirect URL is NOT the safari workaround url
        eq_(response, fb_redirect.return_value)
        ok_(fb_redirect.call_args[0][1] != workaround_url)

    @patch('affiliates.facebook.views.fb_redirect')
    def test_no_authorization(self, fb_redirect, update_user_info):
        """
        If the user has yet to authorize the app, redirect them to the pre-auth
        promo page.
        """
        fb_redirect.return_value = HttpResponse('blah')
        payload = create_payload(user_id=None)
        response = self.load_app(payload)

        eq_(response, fb_redirect.return_value)
        with self.activate('en-US'):
            ok_(fb_redirect.call_args[0][1]
                .endswith(reverse('facebook.pre_auth_promo')))

    @patch.object(FacebookUser, 'is_new', False)
    @patch('affiliates.facebook.views.fb_redirect')
    def test_has_authorization(self, fb_redirect, update_user_info):
        """
        If the user has authorized the app and isn't new, redirect to the main
        banner view.
        """
        fb_redirect.return_value = HttpResponse('blah')
        payload = create_payload(user_id=1)
        response = self.load_app(payload)

        # Assert that the return value of fb_redirect was returned, and that
        # fb_redirect was given a url that ends with the banner_list url.
        eq_(response, fb_redirect.return_value)
        with self.activate('en-US'):
            ok_(fb_redirect.call_args[0][1]
                .endswith(reverse('facebook.banner_list')))

    @patch('affiliates.facebook.views.login')
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

    @patch('affiliates.facebook.views.login')
    def test_country_missing(self, login, update_user_info):
        """
        If the user's country is not included in the signed_request, keep their
        old country value intact.
        """
        user = FacebookUserFactory.create(country='us')
        payload = create_payload(user_id=user.id)
        del payload['user']['country']
        self.load_app(payload)

        eq_(login.called, True)
        eq_(login.call_args[0][1].country, 'us')


class PreAuthPromoTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _pre_auth_promo(self, locale='en-US'):
        request = self.factory.get('/')
        request.locale = locale

        with patch('affiliates.facebook.views.render') as render:
            response = views.pre_auth_promo(request)
            response.context = render.call_args[0][2]

        return response

    def test_locale_banners(self):
        """Ensure that the banners used by the page match the user's locale."""
        banner1 = FacebookBannerLocaleFactory.create(locale='fr').banner
        banner2 = FacebookBannerLocaleFactory.create(locale='fr').banner
        FacebookBannerLocaleFactory.create(locale='en-US')
        response = self._pre_auth_promo('fr')

        eq_(list(response.context['banners']), [banner1, banner2])

    def test_6_banners(self):
        """Only 6 banners should be included in the banner set."""
        for k in range(10):
            FacebookBannerLocaleFactory.create(locale='en-US')
        response = self._pre_auth_promo('en-US')

        eq_(len(response.context['banners']), 6)

    @patch.object(settings, 'LANGUAGE_CODE', 'fr')
    def test_default_locale(self):
        """
        If no banners are available in the requested locale, default to the
        site's default language code.
        """
        banner1 = FacebookBannerLocaleFactory.create(locale='fr').banner
        banner2 = FacebookBannerLocaleFactory.create(locale='fr').banner
        response = self._pre_auth_promo('pt-BR')

        eq_(list(response.context['banners']), [banner1, banner2])


class DeauthorizeTest(TestCase):
    def deauthorize(self, payload):
        """
        Runs the deauthorize view. If payload is None, it will not be
        passed to the view. If it is False, it will fail to be decoded.
        Otherwise, it will be used as the payload.
        """
        post_data = {}
        if payload is not None:
            post_data['signed_request'] = 'signed_request'

        with patch('affiliates.facebook.views.decode_signed_request') as decode:
            if payload:
                decode.return_value = payload
            else:
                decode.return_value = None

            return self.client.post(reverse('facebook.deauthorize'), post_data)

    def test_no_signed_request(self):
        """If no signed request is provided, return a 400 Bad Request."""
        response = self.deauthorize(None)
        eq_(response.status_code, 400)

    def test_invalid_signed_request(self):
        """If the signed request is invalid, return a 400 Bad Request."""
        response = self.deauthorize(False)
        eq_(response.status_code, 400)

    def test_user_does_not_exist(self):
        """
        If the supplied user id doesn't match an existing user, return a 404 Not
        Found.
        """
        response = self.deauthorize({'user_id': 999})
        eq_(response.status_code, 404)

    @patch.object(FacebookUser.objects, 'purge_user_data')
    def test_valid_user(self, purge_user_data):
        """
        If the supplied user id is valid, call purge_user_data with the user.
        """
        user = FacebookUserFactory.create()
        response = self.deauthorize({'user_id': user.id})
        eq_(response.status_code, 200)
        purge_user_data.assert_called_with(user)


class CreateBannerTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        self.client.fb_login(self.user)

    def banner_create(self, **post_data):
        """Execute banner_create view. kwargs are POST arguments."""
        with self.activate('en-US'):
            return self.client.post(reverse('facebook.banner_create'),
                                    post_data)

    @patch('affiliates.facebook.views.generate_banner_instance_image.delay')
    def test_use_profile_image(self, delay):
        """
        If the user checked `use_profile_image`, create a banner instance,
        trigger the celery task and return a 202 Accepted.
        """
        banner = FacebookBannerLocaleFactory.create(locale='en-us').banner
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
        banner = FacebookBannerLocaleFactory.create(locale='en-us').banner
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
        banner = FacebookBannerLocaleFactory.create(locale='en-us').banner
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
                                     format='text', country='us',
                                     source_url=ANY)

    @patch('affiliates.facebook.views.log')
    def test_basket_error_log(self, log, subscribe):
        """If basket throws an exception, log it and return a 200 OK."""
        subscribe.side_effect = basket.BasketException
        response = self.subscribe(email='test@example.com', country='us',
                                  format='text', privacy_policy_agree=True)
        eq_(response.status_code, 200)
        ok_(log.error.called)


@patch.object(settings, 'FACEBOOK_DOWNLOAD_URL', 'http://mozilla.org')
class FollowBannerLinkTests(TestCase):
    def follow_link(self, instance_id, **extra):
        with self.activate('en-US'):
            return self.client.get(reverse('facebook.banners.link',
                                           args=[instance_id]),
                                   **extra)

    def test_instance_does_not_exist(self):
        """
        If the requested banner instance does not exist, return the default
        redirect.
        """
        response = self.follow_link(999)
        self.assert_redirects(response, 'http://mozilla.org')

    @patch('affiliates.facebook.views.add_click')
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

    @patch('affiliates.facebook.views.add_click')
    def test_facebook_bot_no_click(self, add_click):
        """If the request is coming from a facebook bot, do not add a click."""
        instance = FacebookBannerInstanceFactory.create(
            banner__link='http://allizom.org')
        response = self.follow_link(instance.id,
                                    HTTP_USER_AGENT=FACEBOOK_USER_AGENT)
        self.assert_redirects(response, 'http://allizom.org')
        ok_(not add_click.delay.called)


class BannerListTests(TestCase):
    def banner_list(self):
        with self.activate('en-US'):
            return self.client.get(reverse('facebook.banner_list'))

    @patch.object(FacebookUser, 'is_new', True)
    def test_new_user_first_run(self):
        """If the logged in user is new, redirect them to the first run page."""
        user = FacebookUserFactory.create()
        self.client.fb_login(user)

        response = self.banner_list()
        self.assertTemplateUsed(response, 'facebook/first_run.html')

    @patch.object(FacebookUser, 'is_new', False)
    def test_old_user_banner_list(self):
        """If the logged in user is not new, render the banner list page."""
        user = FacebookUserFactory.create()
        self.client.fb_login(user)

        response = self.banner_list()
        self.assertTemplateUsed(response, 'facebook/banner_list.html')


@patch.object(settings, 'FACEBOOK_APP_URL', 'http://mozilla.org')
@patch('affiliates.facebook.views.messages.success')
class PostBannerShareTest(TestCase):
    def post_banner_share(self, **params):
        with self.activate('en-US'):
            return self.client.get(reverse('facebook.post_banner_share'),
                                   params)

    def test_no_post_id(self, success):
        """If no post_id parameter is provided, don't add a success message."""
        response = self.post_banner_share()
        self.assert_redirects(response, 'http://mozilla.org')
        ok_(not success.called)

    def test_post_id(self, success):
        """If no post_id parameter is provided, don't add a success message."""
        response = self.post_banner_share(post_id=999)
        self.assert_redirects(response, 'http://mozilla.org')
        ok_(success.called)


class BannerDeleteTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        self.client.fb_login(self.user)
        FacebookBannerInstanceFactory.create(user=self.user)

    def _delete(self, **kwargs):
        with self.activate('en-US'):
            return self.client.post(reverse('facebook.banners.delete'), kwargs)

    def test_dont_delete_if_user_doesnt_own_banner(self):
        instance = FacebookBannerInstanceFactory.create()
        self._delete(banner_instance=instance.id)
        ok_(FacebookBannerInstance.objects.filter(id=instance.id).exists())

    def test_delete_if_user_owns_banner(self):
        instance = FacebookBannerInstanceFactory.create(user=self.user)
        self._delete(banner_instance=instance.id)
        ok_(not FacebookBannerInstance.objects.filter(id=instance.id).exists())


class StatsTests(TestCase):
    def setUp(self):
        self.user = FacebookUserFactory.create()
        self.client.fb_login(self.user)

    def _stats(self, year, month):
        with self.activate('en-US'):
            return self.client.get(reverse('facebook.stats',
                                           args=[year, month]))

    def test_placeholder_400(self):
        """
        If a placeholder value is used for the year or month, return a 400 Bad
        Request.
        """
        eq_(self._stats(':year:', 2).status_code, 400)
        eq_(self._stats(2012, ':month:').status_code, 400)
        eq_(self._stats(':year:', ':month:').status_code, 400)


class PostInviteTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _post_invite(self, **kwargs):
        return views.post_invite(self.factory.get('/', data=kwargs))

    @patch('affiliates.facebook.views.messages')
    def test_no_success(self, messages):
        """If the success parameter isn't passed via GET, do not add a success message."""
        self._post_invite()
        ok_(not messages.success.called)

    @patch('affiliates.facebook.views.messages')
    def test_success(self, messages):
        """If the success parameter is passed via GET, add a success message."""
        self._post_invite(success='1')
        ok_(messages.success.called)
