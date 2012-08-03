from django.conf import settings


def shared_settings(request):
    """
    Adds a few shared settings for the Facebook app to the template context.
    """
    return {'FACEBOOK_DOWNLOAD_URL': settings.FACEBOOK_DOWNLOAD_URL,
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
            'FACEBOOK_APP_URL': settings.FACEBOOK_APP_URL}
