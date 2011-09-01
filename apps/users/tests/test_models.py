from django.contrib.auth.models import User
from django.core import mail
from nose.tools import eq_, ok_
from test_utils import TestCase

from badges.models import BadgeInstance
from users.models import RegisterProfile
from users.tests.test_forms import activation_form


class RegisterProfileTests(TestCase):
    fixtures = ['registration_profiles.json', 'registered_users.json']

    def setUp(self):
        self.p = RegisterProfile.objects.create_profile('TestUser',
                                                        'test@example.com',
                                                        'asdfasdf')

    def test_email_activation_code(self):
        """Creating a RegisterProfile sends an activation email."""
        eq_(len(mail.outbox), 1)
        ok_(('activate/%s' % self.p.activation_key) in mail.outbox[0].body)

    def test_password_hash(self):
        """Passwords in RegisterProfile are hashed with sha512."""
        ok_(self.p.password.startswith('sha512'))

    def test_activation_password(self):
        """Activating a user transfers the password correctly."""
        form = activation_form(activation_key=self.p.activation_key)
        form.is_valid()

        u = RegisterProfile.objects.activate_profile(self.p.activation_key,
                                                     form)
        ok_(u.check_password('asdfasdf'))

    def test_activate_expired(self):
        """An expired(or already activated) account cannot be activated."""
        key = (User.objects.get(username='mkelly').registerprofile
               .activation_key)
        form = activation_form(activation_key=key)
        form.is_valid()

        ok_(not RegisterProfile.objects.activate_profile(key, form))


class UserTests(TestCase):
    fixtures = ['banners']

    def test_has_created_badges(self):
        user = User.objects.get(pk=1)
        ok_(not user.has_created_badges())

        BadgeInstance.objects.create(user=user, badge_id=1)
        ok_(user.has_created_badges())
