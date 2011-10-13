from django.contrib.auth.models import User
from django.core import mail

import tower
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import BadgeInstance
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

    def test_activation_locale_detect(self):
        p = self._profile()

        # Activate french and check if the locale was set correctly
        tower.activate('fr')
        u = RegisterProfile.objects.activate_profile(p.activation_key)
        eq_(u.get_profile().locale, 'fr')

class UserTests(TestCase):
    fixtures = ['banners']

    def test_has_created_badges(self):
        user = User.objects.get(pk=2)
        ok_(not user.has_created_badges())

        BadgeInstance.objects.create(user=user, badge_id=1)
        ok_(user.has_created_badges())
