from django.core import mail, management

from nose.tools import eq_, ok_
from test_utils import TestCase


class ResendActivationTests(TestCase):
    fixtures = ['registration_profiles']

    def test_send_emails(self):
        """
        When the cronjob is run, emails are sent out to all emails in the
        RegisterProfile table.
        """
        management.call_command('cron', 'resend_activation')
        eq_(len(mail.outbox), 2)

        emails = []
        for email in mail.outbox:
            emails += email.to

        ok_('mkelly@example.com' in emails)
        ok_('linus@example.org' in emails)
