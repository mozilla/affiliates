from django.test.client import RequestFactory

from nose.tools import eq_, ok_

from facebook.forms import (FacebookAccountLinkForm, FacebookBannerInstanceForm,
                            LeaderboardFilterForm)
from facebook.tests import (FacebookBannerFactory, FacebookBannerLocaleFactory,
                            FacebookUserFactory)
from shared.tests import TestCase
from users.tests import UserFactory


class FacebookBannerInstanceFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def form(self, locale, *form_args, **form_kwargs):
        request = self.factory.get('/')
        if locale is not None:
            request.locale = locale
        return FacebookBannerInstanceForm(request, *form_args, **form_kwargs)

    def test_no_locale(self):
        """
        If the request has no set locale, the form should accept any banner in
        any locale.
        """
        fr_banner = FacebookBannerFactory.create()
        FacebookBannerLocaleFactory.create(banner=fr_banner, locale='fr')
        en_banner = FacebookBannerFactory.create()
        FacebookBannerLocaleFactory.create(banner=en_banner, locale='en-us')

        form = self.form(None, {'text': 'asdf', 'banner': fr_banner.id})
        ok_(form.is_valid())

        form = self.form(None, {'text': 'asdf', 'banner': en_banner.id})
        ok_(form.is_valid())

    def test_with_locale(self):
        """
        If the request has a set locale, the form should only accept banners
        available in that locale.
        """
        fr_banner = FacebookBannerFactory.create()
        FacebookBannerLocaleFactory.create(banner=fr_banner, locale='fr')
        en_banner = FacebookBannerFactory.create()
        FacebookBannerLocaleFactory.create(banner=en_banner, locale='en-us')

        form = self.form('fr', {'text': 'asdf', 'banner': fr_banner.id})
        ok_(form.is_valid())

        form = self.form('fr', {'text': 'asdf', 'banner': en_banner.id})
        ok_(not form.is_valid())


class FacebookAccountLinkFormTests(TestCase):
    def test_affiliates_email_validation(self):
        """
        The affiliates_email field is only valid if an Affiliates user exists
        with the specified email address.
        """
        form = FacebookAccountLinkForm({'affiliates_email': 'dne@example.com'})
        eq_(form.is_valid(), False)

        user = UserFactory.create()
        form = FacebookAccountLinkForm({'affiliates_email': user.email})
        eq_(form.is_valid(), True)


class LeaderboardFilterFormTests(TestCase):
    def test_get_top_users(self):
        """
        Test that get_top_users, er, gets the top users ranked by
        leaderboard_position.
        """
        user1 = FacebookUserFactory.create(leaderboard_position=1)
        user2 = FacebookUserFactory.create(leaderboard_position=2)
        user3 = FacebookUserFactory.create(leaderboard_position=3)

        form = LeaderboardFilterForm()
        eq_([user1, user2, user3], list(form.get_top_users()))

    def test_exclude_unranked_users(self):
        """
        If a user has a leaderboard position of -1, do not include them in the
        top users list.
        """
        user1 = FacebookUserFactory.create(leaderboard_position=1)
        FacebookUserFactory.create(leaderboard_position=-1)
        user3 = FacebookUserFactory.create(leaderboard_position=2)

        form = LeaderboardFilterForm()
        eq_([user1, user3], list(form.get_top_users()))

    def test_filter_country(self):
        """
        If the country field is set, only return users within that country.
        """
        user1 = FacebookUserFactory.create(leaderboard_position=1, country='us')
        FacebookUserFactory.create(leaderboard_position=2, country='fr')
        user3 = FacebookUserFactory.create(leaderboard_position=3, country='us')

        form = LeaderboardFilterForm({'country': 'us'})
        eq_([user1, user3], list(form.get_top_users()))
