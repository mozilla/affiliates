import sys

try:
    from .local import *
except ImportError, exc:
    exc.args = tuple(['%s (did you rename settings/local.py-dist?)' % exc.args[0]])
    raise exc


# Lazily evaluate MIDDLEWARE_CLASSES in order to add middleware based on
# settings like DEBUG or DEV.
# We do this here instead of base.py to avoid having to refer to
# STATIC_MIDDLEWARE_CLASSES everywhere in settings instead of the default.
def lazy_middleware_classes():
    from django.conf import settings
    middleware = settings.STATIC_MIDDLEWARE_CLASSES

    if settings.DEBUG and not settings.TEST:
        middleware.insert(0, 'affiliates.facebook.middleware.FacebookDebugMiddleware')

    return middleware
STATIC_MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES[:]
MIDDLEWARE_CLASSES = lazy(lazy_middleware_classes, list)()


# Import test settings
TEST = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TEST:
    try:
        from .test import *
    except ImportError:
        pass
