import test_utils
from nose.tools import ok_

from users.forms import ActivationForm

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

    fixtures = ['registered_users.json']

    def test_usernames_unique(self):
        """Usernames must be unique."""
        form = activation_form(username='mkelly')
        ok_(not form.is_valid())
        ok_('username' in form.errors)

        form = activation_form(username='unique_user')
        ok_(form.is_valid())

    def test_no_new_password(self):
        """Not specifying a new password is alright."""
        form = activation_form(password=None, password2=None)
        ok_(form.is_valid())

    def test_passwords_must_match(self):
        """New passwords must match."""
        form = activation_form(password='fn5n29vs0', password2='fn5n29vs0')
        ok_(form.is_valid())

        form = activation_form(password='fn5n29vs0', password2='n39vsn20n')
        ok_(not form.is_valid())
