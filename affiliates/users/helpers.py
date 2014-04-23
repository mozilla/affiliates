import urllib
from hashlib import md5

from django.conf import settings
from django.contrib.auth.models import User

from funfactory.helpers import static
from jingo import register

from affiliates.base.utils import absolutify


GRAVATAR_URL = getattr(settings, 'GRAVATAR_URL', 'https://secure.gravatar.com')


@register.function
def gravatar(arg, size=80):
    if isinstance(arg, User):
        email = arg.email
    else:  # Treat as email
        email = arg

    return '{url}/avatar/{email_hash}?{options}'.format(
        url=GRAVATAR_URL,
        email_hash=md5(email.lower()).hexdigest(),
        options=urllib.urlencode({'s': unicode(size), 'd': absolutify(static('img/avatar.jpg'))})
    )
