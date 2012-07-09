from time import time


def create_payload(user_id=None, algorithm='HMAC-SHA256', country='us',
                   locale='en_US'):
    """Creates a signed request payload with the proper structure."""
    payload = {
        'algorithm': algorithm,
        'issued_at': int(time()),
        'user': {
            'country': country,
            'locale': locale
        }
    }

    if user_id:
        payload['user_id'] = user_id
    return payload
