from django.conf import settings

from affiliates.facebook.forms import FacebookAccountLinkForm, NewsletterSubscriptionForm
from affiliates.facebook.models import AppNotification
from affiliates.facebook.utils import in_facebook_app, is_logged_in


def app_context(request):
    """
    Adds context data that is shared across the Facebook app.
    """
    if not in_facebook_app(request):
        return {}

    ctx = {'FACEBOOK_DOWNLOAD_URL': settings.FACEBOOK_DOWNLOAD_URL,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
            'FACEBOOK_CLICK_GOAL': settings.FACEBOOK_CLICK_GOAL}

    # Add account link form.
    if not request.user.is_linked:
        ctx['account_link_form'] = FacebookAccountLinkForm()

    if is_logged_in(request):
        # Add newsletter form to en-US
        if request.locale.startswith('en'):
            ctx['newsletter_form'] = NewsletterSubscriptionForm(
                request.user, auto_id='newsletter_%s')

        # Add notifications
        ctx['app_notifications'] = (AppNotification.objects
                                    .filter(user=request.user))

    return ctx
