from django.contrib.auth.models import User
from django.core import mail

import tower
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import BadgeInstance
from facebook.tests import FacebookAccountLinkFactory
from users.models import RegisterProfile


class RegisterProfileTests(TestCase):
    fixtures = ['registration_profiles.json', 'registered_users.json']

    def _profile(self, name='TestUser', email='test@example.com',
                 password='asdf1234'):
        return RegisterProfile.objects.create_profile(name, email, password)

    def test_email_activation_code(self):
        """Creating a RegisterProfile sends an activation email."""
        p = self._profile()
        eq_(len(mail.outbox), 1)
        ok_(('activate/%s' % p.activation_key) in mail.outbox[0].body)

    def test_password_hash(self):
        """Passwords in RegisterProfile are hashed with sha512."""
        p = self._profile()
        ok_(p.password.startswith('sha512'))

    def test_activation_password(self):
        """Activating a user transfers the password correctly."""
        p = self._profile()
        u = RegisterProfile.objects.activate_profile(p.activation_key)
        ok_(u.check_password('asdf1234'))

    def test_activation_active(self):
        """Test activated users are active."""
        p = self._profile()
        u = RegisterProfile.objects.activate_profile(p.activation_key)
        ok_(u.is_active)

    def test_register_existing_replace(self):
        p = self._profile('Richard Stallman', 'linus@example.org',
                          'trolololol')
        eq_(p.id, 11)


class UserTests(TestCase):
    fixtures = ['banners']

    def test_has_created_badges(self):
        user = User.objects.get(pk=2)
        ok_(not user.has_created_badges())

        BadgeInstance.objects.create(user=user, badge_id=1)
        ok_(user.has_created_badges())

    def test_get_linked_account(self):
        user = User.objects.get(pk=2)
        link = FacebookAccountLinkFactory.create(affiliates_user=user,
                                                 is_active=True)
        eq_(user.get_linked_account(), link.facebook_user)

    def test_get_linked_account_none(self):
        user = User.objects.get(pk=2)
        eq_(user.get_linked_account(), None)

    def test_get_linked_account_inactive(self):
        user = User.objects.get(pk=2)
        FacebookAccountLinkFactory.create(affiliates_user=user, is_active=False)
        eq_(user.get_linked_account(), None)
