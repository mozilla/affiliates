from django.contrib.auth.signals import user_logged_in


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
    request.fb_user = user
    user_logged_in.send(sender=user.__class__, request=request, user=user)
