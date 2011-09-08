import test_utils
from nose.tools import ok_

from users.forms import ActivationForm, EditProfileForm


def activation_form_defaults():
    """Returns a set of default values for testing the activation form."""
    return {'username': 'TestUser', 'country': 'us',
            'locale': 'en-US', 'accept_email': True}


def activation_form(**kwargs):
    """Return an activation form with default values"""
    defaults = activation_form_defaults()
    defaults.update(kwargs)

    return ActivationForm(defaults)


class ActivationFormTests(test_utils.TestCase):
    fixtures = ['registered_users']

    def test_usernames_unique(self):
        """Usernames must be unique."""
        form = activation_form(username='mkelly')
        ok_(not form.is_valid())
        ok_('username' in form.errors)

        form = activation_form(username='unique_user')
        ok_(form.is_valid())


class EditProfileFormTests(test_utils.TestCase):

    def _form(self, **kwargs):
        """Default profile edit form."""
        defaults = {'name': 'Test User', 'locale': 'en-US', 'country': 'us'}
        defaults.update(kwargs)

        return EditProfileForm(defaults)

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

    def test_password_complexity(self):
        # Must include at least 1 number
        form = self._form(password='asdfasdf', password2='asdfasdf')
        ok_(not form.is_valid())

        # Must include at least 1 letter
        form = self._form(password='12341234', password2='12341234')
        ok_(not form.is_valid())

        # Must be at least 8 characters long
        form = self._form(password='as12', password2='as12')
        ok_(not form.is_valid())
