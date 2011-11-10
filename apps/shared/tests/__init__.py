from smtplib import SMTPException

from django.core.mail.backends.base import BaseEmailBackend


class BrokenSMTPBackend(BaseEmailBackend):
    """Simulates an email backend that throws errors."""
    def send_messages(self, email_messages):
        raise SMTPException('Dummy')


def model_ids(models):
    """Generates a list of model ids from a list of model objects."""
    return [m.pk for m in models]
