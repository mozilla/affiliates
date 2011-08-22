import test_utils

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
                                     'password': 'asdfasdf'})
        eq_(200, response.status_code)

        p = RegisterProfile.objects.get(name='newbie')
        assert p.password.startswith('sha512')

        eq_(len(mail.outbox), 1)
        ok_(mail.outbox[0].body.find('activate/%s' % p.activation_key))


    def test_activation(self):
        """Test basic account activation."""
        parameters = activation_form_defaults()
        reg_profile = RegisterProfile.objects.create_profile(
            'TestName', 'a@b.com', 'asdfasdf')

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
