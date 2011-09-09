from smtplib import SMTPException

from django.core.mail.backends.base import BaseEmailBackend


class BrokenSMTPBackend(BaseEmailBackend):
    """Simulates an email backend that throws errors."""
    def send_messages(self, email_messages):
        raise SMTPException('Dummy')
