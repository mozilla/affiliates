from django.test.client import RequestFactory

from nose.tools import eq_, ok_

from facebook.forms import FacebookAccountLinkForm, FacebookBannerInstanceForm
from facebook.tests import FacebookBannerFactory, FacebookBannerLocaleFactory
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
