# Tests should use the dummy cache.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SITE_URL = 'http://badge.mo.com'