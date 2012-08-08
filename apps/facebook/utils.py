import base64
import hashlib
import hmac
import json

import commonware.log


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
