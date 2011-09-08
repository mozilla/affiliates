import test_utils

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from nose.tools import eq_, ok_

from badges.tests import LocalizingClient
from users.models import RegisterProfile
from users.tests.test_forms import activation_form_defaults


class RegisterTests(test_utils.TestCase):

    client_class = LocalizingClient

    def test_new_profile(self):
        """
        Test new user registration.

        A registration profile should be created and an activation email sent.
        """
        response = self.client.post(reverse('users.register'),
                                    {'name': 'newbie',
                                     'email': 'newbie@example.com',
                                     'password': 'asdf1234'})
        eq_(200, response.status_code)

        p = RegisterProfile.objects.get(name='newbie')
        assert p.password.startswith('sha512')

        eq_(len(mail.outbox), 1)
        ok_(mail.outbox[0].body.find('activate/%s' % p.activation_key))

    def test_activation(self):
        """Test basic account activation."""
        parameters = activation_form_defaults()
        reg_profile = RegisterProfile.objects.create_profile(
            'TestName', 'a@b.com', 'asdf1234')

        kwargs = {'activation_key': reg_profile.activation_key}
        response = self.client.post(reverse('users.activate', kwargs=kwargs),
                                    parameters)
        eq_(200, response.status_code)

        # Test relations
        u = User.objects.get(username='TestUser')
        eq_(u.get_profile().name, 'TestName')

    def test_invalid_activation_key(self):
        """Invalid activation keys are redirected to the homepage."""
        kwargs = {'activation_key': "invalid_key"}
        response = self.client.get(reverse('users.activate',
                                           kwargs=kwargs))

        eq_(302, response.status_code)
        eq_('http://testserver/', response['Location'])


class LoginTests(test_utils.TestCase):
    client_class = LocalizingClient
    fixtures = ['registered_users']

    def test_basic_login(self):
        """Test that a basic login works."""
        parameters = {'username': 'mkelly', 'password': 'asdfasdf'}
        response = self.client.post(reverse('users.login'), parameters)

        ok_(response.cookies[settings.SESSION_COOKIE_NAME])
        eq_(response.cookies[settings.SESSION_COOKIE_NAME]['expires'], '')

    def test_remembered_login(self):
        """
        Test that logging in with "Remember me" checked sets the
        session expiration.
        """
        parameters = {'username': 'mkelly', 'password': 'asdfasdf',
                      'remember_me': True}
        response = self.client.post(reverse('users.login'), parameters)

        ok_(response.cookies[settings.SESSION_COOKIE_NAME]['expires'])


class EditProfileTests(test_utils.TestCase):
    client_class = LocalizingClient
    fixtures = ['registered_users']

    def setUp(self):
        self.client.login(username='mkelly', password='asdfasdf')

    def _params(self, **kwargs):
        """Default arguments for profile edit form."""
        defaults = {'name': 'Test User', 'locale': 'en-US', 'country': 'us'}
        defaults.update(kwargs)

        return defaults

    def test_basic_edit(self):
        parameters = self._params(name='Honey Badger', state="Doesn't care")
        self.client.post(reverse('users.edit.profile'), parameters)

        user = User.objects.get(pk=1)
        eq_(user.get_profile().name, 'Honey Badger')
        eq_(user.get_profile().state, "Doesn't care")

    def test_change_password(self):
        parameters = self._params(password='asdf1234', password2='asdf1234')
        self.client.post(reverse('users.edit.profile'), parameters)

        user = User.objects.get(pk=1)
        ok_(user.check_password('asdf1234'))
