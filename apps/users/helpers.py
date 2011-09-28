import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.hashcompat import md5_constructor

from jingo import register
from jinja2 import Markup

from shared.utils import absolutify
from users.models import UserProfile


GRAVATAR_URL = getattr(settings, 'GRAVATAR_URL', 'http://www.gravatar.com')
DEFAULT_GRAVATAR = absolutify(settings.DEFAULT_GRAVATAR, https=True)


@register.function
def gravatar_url(arg, size=80):
    if isinstance(arg, User):
        email = arg.email
    else:  # Treat as email
        email = arg

    url = '%s/avatar/%s?%s' % (
        GRAVATAR_URL, md5_constructor(email.lower()).hexdigest(),
        urllib.urlencode({'s': str(size), 'default': DEFAULT_GRAVATAR}))

    return url


@register.function
def gravatar_img(arg, size=80):
    return Markup('<img src="%s">' % gravatar_url(arg, size=size))



@register.function
def display_name(user):
    """Return a display name if set, else the username."""
    try:  # Also mostly for tests.
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        return user.username
    return profile.display_name if profile.display_name else user.username
