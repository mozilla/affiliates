import base64
import hashlib
import hmac
import json
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.utils.translation import get_language

import commonware.log
import tower


log = commonware.log.getLogger('a.facebook')


def decode_signed_request(signed_request, secret):
    """
    Return a dict with data from the request payload, or None if the request is
    invalid.
    """
    try:
        encoded_signature, encoded_json = signed_request.split('.')
        signature = modified_url_b64decode(encoded_signature)
        payload = json.loads(modified_url_b64decode(encoded_json))
    except ValueError:
        log.warning('Incorrectly formatted signed request: {0}'
                    .format(signed_request))
        return None

    # Verify signature using app secret.
    if payload['algorithm'] != 'HMAC-SHA256':
        log.warning('Unknown algorithm for signed request. Expected '
                    'HMAC-SHA256: {0}'.format(signed_request))
        return None

    digest = hmac.new(secret, encoded_json, hashlib.sha256).digest()
    if digest != signature:
        log.warning('Signature verification failed: {0}'.format(signed_request))
        return None

    return payload


def modified_url_b64decode(b64string):
    """
    Decodes a base64 string stored in a modified format for URLs, where there is
    no padding and the + and / symbols are replaced by - and _ respectively.
    """
    # Add padding and force to ASCII (since base64 encoding doesn't use unicode)
    if isinstance(b64string, unicode):
        b64string = b64string.encode('utf-8')
    b64string = b64string + ('=' * (4 - len(b64string) % 4))
    return base64.b64decode(b64string, '-_')


def in_facebook_app(request):
    """
    Determine if the given request points to a page within the Facebook app.
    """
    return request.path.startswith('/fb')


def is_logged_in(request):
    """
    Determine if the given request contains an active Facebook user session.
    """
    from affiliates.facebook.models import FacebookUser
    return (request.user.is_authenticated() and
            isinstance(request.user, FacebookUser))


def is_facebook_bot(request):
    """Check the request's User-Agent against the Facebook bot's User-Agent."""
    ua = request.META.get('HTTP_USER_AGENT', '')
    return ua.startswith('facebookexternalhit')


def current_hour():
    """Return a datetime representing the current hour."""
    now = datetime.now()
    return datetime(now.year, now.month, now.day, now.hour)


def activate_locale(request, locale):
    """
    Activates the specified locale if it is in the list of supported locales.
    """
    # HACK: It's not totally clear to me where Django or tower do the matching
    # that equates locales like es-LA to es, and I'm scared enough of getting it
    # wrong to want to avoid it for the first release. So instead, we'll
    # activate the requested locale, and then check what locale got chosen by
    # django as the usable locale, and match that against our locale whitelist.
    # TODO: Properly filter out locales prior to calling activate.
    tower.activate(locale)
    lang = get_language()
    if not settings.DEV and lang not in settings.FACEBOOK_LOCALES:
        lang = lang.split('-')[0]
        tower.activate(lang)
        lang = get_language()
        if lang not in settings.FACEBOOK_LOCALES:
            lang = 'en-us'
            tower.activate(lang)

    request.locale = lang


def fb_redirect(request, url, top_window=False):
    """
    Return a response that will redirect a user within the Facebook app to the
    given URL.
    """
    return render(request, 'facebook/redirect.html',
                  {'url': url, 'top_window': top_window})
