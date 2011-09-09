from django.conf import settings
from django.core import mail
from django.forms import Form

from mock import patch
from nose.tools import eq_, ok_
from test_utils import TestCase

from users import forms


def activation_form_defaults():
    """Returns a set of default values for testing the activation form."""
    return {'username': 'TestUser', 'country': 'us',
            'locale': 'en-US', 'accept_email': True}


def activation_form(**kwargs):
    """Return an activation form with default values"""
    defaults = activation_form_defaults()
    defaults.update(kwargs)

    return forms.ActivationForm(defaults)


class ActivationFormTests(TestCase):
    fixtures = ['registered_users']

    def test_usernames_unique(self):
        """Usernames must be unique."""
        form = activation_form(username='mkelly')
        ok_(not form.is_valid())
        ok_('username' in form.errors)

        form = activation_form(username='unique_user')
        ok_(form.is_valid())


class EditProfileFormTests(TestCase):

    def _form(self, **kwargs):
        """Default profile edit form."""
        defaults = {'name': 'Test User', 'locale': 'en-US', 'country': 'us'}
        defaults.update(kwargs)

        return forms.EditProfileForm(defaults)

    def test_no_new_password(self):
        """Not specifying a new password is alright."""
        form = self._form(password=None, password2=None)
        ok_(form.is_valid())

    def test_passwords_must_match(self):
        """New passwords must match."""
        form = self._form(password='fn5n29vs0', password2='fn5n29vs0')
        ok_(form.is_valid())

        form = self._form(password='fn5n29vs0', password2='n39vsn20n')
        ok_(not form.is_valid())


class PasswordFieldTests(TestCase):
    class Form(Form):
        password = forms.PasswordField()

    def _form(self, pw):
        return self.Form({'password': pw})

    def test_password_complexity(self):
        # Must include at least 1 number
        form = self._form('asdfasdf')
        ok_(not form.is_valid())

        # Must include at least 1 letter
        form = self._form('12341234')
        ok_(not form.is_valid())

        # Must be at least 8 characters long
        form = self._form('as12')
        ok_(not form.is_valid())


class PasswordResetFormTests(TestCase):
    fixtures = ['registered_users']

    def _form(self, email):
        return forms.PasswordResetForm({'email': email})

    def test_basic(self):
        form = self._form('mkelly@mozilla.com')
        ok_(form.is_valid())

        # Check that email was sent
        form.send()
        ok_('accounts/pwreset/1' in mail.outbox[0].body)

    def test_no_user_found(self):
        form = self._form('honey@badger.com')
        ok_(not form.is_valid())

    @patch.object(settings, 'EMAIL_BACKEND', 'shared.tests.BrokenSMTPBackend')
    def test_broken_email_backend(self):
        form = self._form('mkelly@mozilla.com')
        ok_(not form.send())
        eq_(form._errors['email'][0], forms.ERROR_SEND_EMAIL)


class SetPasswordFormTests(TestCase):
    fixtures = ['registered_users']

    def _form(self, pw, pw2):
        return forms.SetPasswordForm({'new_password1': pw,
                                      'new_password2': pw2})

    def passwords_must_match(self):
        form = self._form('asdf1234', 'asdf1234')
        ok_(form.is_valid())

        form = self._form('asdf1234', 'qwer5678')
        ok_(not form.is_valid())
