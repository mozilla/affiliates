import json
import os
from datetime import datetime

from django.conf import settings
from django.core import mail
from django.core.files import File
from django.test.client import RequestFactory

import requests
from mock import Mock, patch
from nose.tools import eq_, ok_

from facebook.models import (FacebookAccountLink, FacebookBanner,
                             FacebookBannerInstance, FacebookClickStats,
                             FacebookUser)
from facebook.tests import (FacebookAccountLinkFactory,
                            FacebookBannerInstanceFactory,
                            FacebookBannerLocaleFactory,
                            FacebookClickStatsFactory, FacebookUserFactory,
                            path)
from shared.tests import TestCase
from users.tests import UserFactory


def _r(content):
    response = requests.Response()
    response._content = content
    return response


@patch.object(settings, 'FACEBOOK_CLICK_GOAL_EMAIL', 'admin@example.com')
class FacebookUserManagerTests(TestCase):
    manager = FacebookUser.objects

    def user(self, **kwargs):
        user = FacebookUserFactory(**kwargs)
        user.save = Mock()
        return user

    @patch.object(requests, 'get')
    def test_request_error(self, get):
        """If requests encounters an error, do nothing."""
        get.side_effect = requests.exceptions.RequestException
        user = self.user()
        self.manager.update_user_info(user)
        ok_(not user.save.called)

    @patch.object(requests, 'get')
    def test_json_error(self, get):
        """If there is an error parsing Facebook's JSON, do nothing."""
        get.return_value = _r('malformed.json')
        user = self.user()

        self.manager.update_user_info(user)
        ok_(not user.save.called)

    @patch.object(requests, 'get')
    def test_successful_update(self, get):
        """
        If the JSON retrieved from Facebook is valid, update the user object.
        """
        get.return_value = _r(json.dumps({'locale': 'en-US', 'name': 'Fred'}))
        user = self.user(full_name='Rob', first_name='Bob')

        self.manager.update_user_info(user)
        ok_(user.save.called)

        eq_(user.locale, 'en-US')  # Empty value replaced.
        eq_(user.full_name, 'Fred')  # Value replaced.
        eq_(user.first_name, 'Bob')  # Value preserved.
        eq_(user.last_name, '')  # Empty value preserved.

    def test_purge_email(self):
        """
        If a user is being purged and has banners that have passed ad review,
        send an email to the admin with info about the ads that need to be
        removed.
        """
        user = FacebookUserFactory.create()
        instance1 = FacebookBannerInstanceFactory.create(
            user=user, review_status=FacebookBannerInstance.PASSED)
        instance2 = FacebookBannerInstanceFactory.create(
            user=user, review_status=FacebookBannerInstance.PASSED)
        instance3 = FacebookBannerInstanceFactory.create(
            user=user, review_status=FacebookBannerInstance.FAILED)

        user_id = 'User ID: %s' % user.id
        instance1_id = 'Banner Instance ID: %s' % instance1.id
        instance2_id = 'Banner Instance ID: %s' % instance2.id
        instance3_id = 'Banner Instance ID: %s' % instance3.id
        self.manager.purge_user_data(user)

        eq_(len(mail.outbox), 1)
        msg = mail.outbox[0]
        ok_('admin@example.com' in msg.to)
        ok_(user_id in msg.body)
        ok_(instance1_id in msg.body)
        ok_(instance2_id in msg.body)
        ok_(not instance3_id in msg.body)

    def test_purge_delete_images(self):
        """
        If there are any custom-generated images for a user's banner instances,
        they must be deleted.
        """
        user = FacebookUserFactory.create()
        instance = FacebookBannerInstanceFactory.create(user=user)
        with open(path('images', 'banner.png')) as banner:
            instance.custom_image.save('custom.png', File(banner))
        file_path = ''.join((settings.MEDIA_ROOT, instance.custom_image.name))

        self.manager.purge_user_data(user)
        ok_(not os.path.exists(file_path))

    def test_purge_delete_everything(self):
        """Ensure that purge deletes all relevant database entries."""
        fb_user = FacebookUserFactory.create()
        user = UserFactory.create()
        link = FacebookAccountLinkFactory.create(affiliates_user=user,
                                                 facebook_user=fb_user)
        instance = FacebookBannerInstanceFactory.create(user=fb_user)
        personal_items = [(item.__class__, item.id) for item in
                          (fb_user, link, instance)]

        self.manager.purge_user_data(fb_user)
        for klass, id in personal_items:
            eq_(klass.objects.filter(id=id).exists(), False)


class FacebookAccountLinkManagerTests(TestCase):
    manager = FacebookAccountLink.objects

    def setUp(self):
        self.factory = RequestFactory()

    def test_create_link_no_account(self):
        """
        If no user exists with the given email, create_link should return False.
        """
        fb_user = FacebookUserFactory.create()
        eq_(self.manager.create_link(fb_user, 'does.not.exist@example.com'),
            False)

    def test_create_link_active_link(self):
        """If an active link already exists, create_link should return False."""
        link = FacebookAccountLinkFactory.create(is_active=True)
        result = self.manager.create_link(link.facebook_user,
                                          link.affiliates_user.email)
        eq_(result, False)

        # Test an active link with a different email address.
        user = UserFactory.create()
        result = self.manager.create_link(link.facebook_user, user.email)
        eq_(result, False)

    def test_create_link_affiliates_already_linked(self):
        """
        If the Affiliates user is already linked to another account, create_link
        should return False.
        """
        link = FacebookAccountLinkFactory.create(is_active=True)
        fb_user = FacebookUserFactory.create()
        result = self.manager.create_link(fb_user, link.affiliates_user.email)
        eq_(result, False)

    def test_create_link_inactive_link(self):
        """
        If a link exists but is inactive, create_link should return the link.
        """
        link = FacebookAccountLinkFactory.create(is_active=False)
        result = self.manager.create_link(link.facebook_user,
                                          link.affiliates_user.email)
        eq_(result, link)
        eq_(link.is_active, False)

    def test_create_link_success(self):
        """
        If no link exists, create_link should create one and save it to the
        database.
        """
        fb_user = FacebookUserFactory.create()
        user = UserFactory.create()
        link = self.manager.create_link(fb_user, user.email)
        eq_(link.affiliates_user, user)
        eq_(link.facebook_user, fb_user)
        eq_(link.is_active, False)
        ok_(self.manager.filter(pk=link.pk).exists())

    def test_send_activation_email(self):
        request = self.factory.get('/')
        link = FacebookAccountLinkFactory.create()

        with self.activate('en-US'):
            self.manager.send_activation_email(request, link)
            eq_(len(mail.outbox), 1)
            eq_(mail.outbox[0].subject, 'Link your Firefox Affiliates account')
            ok_(link.activation_link in mail.outbox[0].body)

    def test_activate_link_invalid_code(self):
        """If the activation code is invalid, return None."""
        result = self.manager.activate_link('does.not.exist')
        eq_(result, None)

    def test_activate_link_active_link(self):
        """If the code corresponds to an already-active link, return None."""
        link = FacebookAccountLinkFactory.create(is_active=True)
        result = self.manager.activate_link(link.activation_code)
        eq_(result, None)

    def test_activate_link_verify_failure(self):
        """If the activation_code fails to verify, return None."""
        link = FacebookAccountLinkFactory.create(activation_code='invalid')
        result = self.manager.activate_link(link.activation_code)
        eq_(result, None)

    def test_activate_link_success(self):
        """If the activation_code is valid, return the new, active link."""
        link = FacebookAccountLinkFactory.create(is_active=False)
        result = self.manager.activate_link(link.activation_code)
        eq_(result, link)
        eq_(result.is_active, True)


class FacebookClickStatsManagerTests(TestCase):
    manager = FacebookClickStats.objects

    def _mkstats(self, user, year, month, clicks):
        hour = datetime(year, month, 1, 0)
        return FacebookClickStatsFactory.create(banner_instance__user=user,
                                                hour=hour, clicks=clicks)

    def test_total_for_month(self):
        """Test that the click sum logic is correct."""
        user = FacebookUserFactory.create()
        self._mkstats(user, 2012, 5, 5)
        self._mkstats(user, 2012, 3, 7)
        self._mkstats(user, 2012, 5, 2)
        eq_(self.manager.total_for_month(user, 2012, 5), 7)

    def test_total_for_month_none(self):
        """If there are no clicks for the given month, return 0."""
        user = FacebookUserFactory.create()
        eq_(self.manager.total_for_month(user, 2012, 5), 0)

    def test_total_for_year(self):
        user = FacebookUserFactory.create()
        self._mkstats(user, 2012, 3, 1)
        self._mkstats(user, 2012, 4, 2)
        self._mkstats(user, 2012, 5, 3)
        eq_(self.manager.total_for_user(user), 6)

    def test_total_for_year_none(self):
        """If there are no clicks for the given user, return 0."""
        user = FacebookUserFactory.create()
        eq_(self.manager.total_for_user(user), 0)


class FacebookBannerQuerySetTests(TestCase):
    def test_filter_by_locale_basic(self):
        banner1 = FacebookBannerLocaleFactory.create(locale='en-US').banner
        banner2 = FacebookBannerLocaleFactory.create(locale='en-US').banner
        FacebookBannerLocaleFactory.create(locale='fr').banner
        FacebookBannerLocaleFactory.create(locale='pt-BR').banner
        results = FacebookBanner.objects.all().filter_by_locale('en-US')

        eq_(list(results), [banner1, banner2])

    def test_filter_by_locale_lang(self):
        banner1 = FacebookBannerLocaleFactory.create(locale='en-US').banner
        banner2 = FacebookBannerLocaleFactory.create(locale='en-US').banner
        FacebookBannerLocaleFactory.create(locale='fr').banner
        FacebookBannerLocaleFactory.create(locale='pt-BR').banner

        results = FacebookBanner.objects.all().filter_by_locale('en-AU')
        eq_(list(results), [banner1, banner2])

        results = FacebookBanner.objects.all().filter_by_locale('en')
        eq_(list(results), [banner1, banner2])
