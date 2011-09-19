from django.conf import settings


def login_required(view_func):
    """
    Decorator that redirects a user to the login page if they are not
    logged in.
    """
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        else:
            from shared.utils import redirect
            return redirect(settings.LOGIN_VIEW_NAME)
    return decorator
