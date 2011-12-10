from django.conf import settings
from django.utils.translation import get_language


def l10n(request):
    """Adds language information to template contexts."""
    locale = get_language()
    return {'LOCALE': locale, 'LANGUAGE': settings.LANGUAGES[locale]}
