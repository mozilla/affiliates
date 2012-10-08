from django.conf import settings

from facebook.forms import FacebookAccountLinkForm, NewsletterSubscriptionForm
from facebook.utils import in_facebook_app, is_logged_in


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

    # Add newsletter form
    if is_logged_in(request):
        ctx['newsletter_form'] = NewsletterSubscriptionForm(
            request.user, auto_id='newsletter_%s')

    return ctx
