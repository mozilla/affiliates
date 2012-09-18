from datetime import datetime

from facebook.models import FacebookUser
from facebook.tasks import update_user_info


SESSION_KEY = '_fb_auth_user_id'


def login(request, user):
    """
    Log the given user into the site, creating a session for them.

    Adapted from django.contrib.auth.login.
    """
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != user.id:
            # Logging in as a different user, flush the session.
            request.session.flush()
    else:
        # Logging in, create a new session key.
        request.session.cycle_key()
    request.session[SESSION_KEY] = user.id
    request.user = user

    # Once the user has logged in, we should update their info from the
    # Facebook Graph. If this is not their first time logging in, we'll do it
    # asynchronously.
    last_login = user.last_login
    user.last_login = datetime.now()
    user.save()

    if last_login is None:
        FacebookUser.objects.update_user_info(user)
    else:
        update_user_info.delay(user.id)
