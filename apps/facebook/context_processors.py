from django.conf import settings

from facebook.forms import FacebookAccountLinkForm
from facebook.utils import in_facebook_app


def app_context(request):
    """
    Adds context data that is shared across the Facebook app.
    """
    if not in_facebook_app(request):
        return {}

    ctx = {'FACEBOOK_DOWNLOAD_URL': settings.FACEBOOK_DOWNLOAD_URL,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
            'FACEBOOK_APP_URL': settings.FACEBOOK_APP_URL}

    # Add account link form.
    if not request.user.is_linked:
        ctx['account_link_form'] = FacebookAccountLinkForm()

    return ctx
