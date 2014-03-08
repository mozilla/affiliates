from django.utils.functional import wraps

from affiliates.facebook.utils import is_logged_in
from affiliates.base.utils import redirect


def fb_login_required(func):
    """
    View decorator that checks to see that the user is logged in via Facebook.
    If the user isn't, then we redirect them to the homepage as they most likely
    stumbled onto this part of the site by accident.
    """
    @wraps(func)
    def inner(request, *args, **kwargs):
        if is_logged_in(request):
            return func(request, *args, **kwargs)
        else:
            return redirect('base.home')
    return inner
