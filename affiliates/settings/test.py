# This file contains settings that apply only while the test suite is
# running. If the setting value is important to your test, mock it
# instead of using this.

# Tests should use the dummy cache.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SITE_URL = 'http://badge.mo.com'

# Speed up tests.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Workaround for jingo-minify bug; if TEMPLATE_DEBUG is True during the
# tests, jingo-minify will generate the wrong path to static media due
# to Django forcing DEBUG to be False during tests.
TEMPLATE_DEBUG = False
