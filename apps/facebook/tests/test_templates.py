from funfactory.urlresolvers import reverse
from nose.tools import eq_, ok_

from facebook.tests import AppNotificationFactory, FacebookUserFactory
from shared.tests import TestCase


class BaseTemplateTests(TestCase):
    urls = 'facebook.tests.urls'

    def test_notifications_cleared(self):
        """
        If a page is using the base Facebook template, any AppNotifications for
        the current user should be displayed and then removed from the database.
        """
        user = FacebookUserFactory.create()
        notification1 = AppNotificationFactory.create(user=user)
        notification2 = AppNotificationFactory.create(user=user)

        eq_(len(user.appnotification_set.all()), 2)

        with self.activate('en-US'):
            self.client.fb_login(user)
            response = self.client.get(reverse('facebook.base_test'))

        ok_(notification1.message in response.content)
        ok_(notification2.message in response.content)
        eq_(len(user.appnotification_set.all()), 0)
