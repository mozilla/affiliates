from django.contrib.auth.models import User
from django.core import mail
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import BadgeInstance
from users.models import RegisterProfile


class RegisterProfileTests(TestCase):
    fixtures = ['registration_profiles.json', 'registered_users.json']

    def test_email_activation_code(self):
        """Creating a RegisterProfile sends an activation email."""
        p = RegisterProfile.objects.create_profile('TestUser',
                                                   'test@example.com',
                                                   'asdf1234')
        eq_(len(mail.outbox), 1)
        ok_(('activate/%s' % p.activation_key) in mail.outbox[0].body)

    def test_password_hash(self):
        """Passwords in RegisterProfile are hashed with sha512."""
        p = RegisterProfile.objects.create_profile('TestUser',
                                                   'test@example.com',
                                                   'asdf1234')
        ok_(p.password.startswith('sha512'))

    def test_activation_password(self):
        """Activating a user transfers the password correctly."""
        p = RegisterProfile.objects.create_profile('TestUser',
                                                   'test@example.com',
                                                   'asdf1234')
        u = RegisterProfile.objects.activate_profile(p.activation_key)
        ok_(u.check_password('asdf1234'))

    def test_activation_active(self):
        """Test activated users are active."""
        p = RegisterProfile.objects.create_profile('TestUser',
                                                   'test@example.com',
                                                   'asdf1234')
        u = RegisterProfile.objects.activate_profile(p.activation_key)
        ok_(u.is_active)

    def test_register_existing_replace(self):
        profile = RegisterProfile.objects.create_profile('Richard Stallman',
                                                         'linus@example.org',
                                                         'trolololol')
        eq_(profile.id, 11)


class UserTests(TestCase):
    fixtures = ['banners']

    def test_has_created_badges(self):
        user = User.objects.get(pk=1)
        ok_(not user.has_created_badges())

        BadgeInstance.objects.create(user=user, badge_id=1)
        ok_(user.has_created_badges())
