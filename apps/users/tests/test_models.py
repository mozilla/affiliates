import test_utils

from django.core import mail
from nose.tools import eq_, ok_

from users.models import RegisterProfile
from users.tests import activation_form


class RegisterProfileTests(test_utils.TestCase):
    fixtures = ['registration_profiles.json']

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
