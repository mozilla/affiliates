from funfactory.urlresolvers import reverse
from nose.tools import eq_

from affiliates.facebook.tests import AppNotificationFactory, FacebookUserFactory
from affiliates.shared.tests import TestCase


class BaseTemplateTests(TestCase):
    urls = 'affiliates.facebook.tests.urls'

    def test_notifications_cleared(self):
        """
        If a page is using the base Facebook template, any AppNotifications for
        the current user should be displayed and then removed from the database.
        """
        user = FacebookUserFactory.create()
        AppNotificationFactory.create(user=user)
        AppNotificationFactory.create(user=user)

        eq_(len(user.appnotification_set.all()), 2)

        with self.activate('en-US'):
            self.client.fb_login(user)
            self.client.get(reverse('facebook.base_test'))

        eq_(len(user.appnotification_set.all()), 0)
