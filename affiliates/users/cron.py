import cronjobs

from affiliates.users.models import RegisterProfile, ACTIVATION_EMAIL_SUBJECT


@cronjobs.register
def resend_activation():
    """
    Resends the activation email to every user who hasn't activated their
    account.
    """
    for profile in RegisterProfile.objects.all():
        RegisterProfile.objects._send_email('users/email/activation_email.html',
                                            ACTIVATION_EMAIL_SUBJECT, profile)
