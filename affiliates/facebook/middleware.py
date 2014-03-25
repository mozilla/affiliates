from funfactory.urlresolvers import Prefixer

from affiliates.facebook.auth import SESSION_KEY
from affiliates.facebook.models import AnonymousFacebookUser, FacebookUser
from affiliates.facebook.utils import activate_locale, in_facebook_app


class FacebookAuthenticationMiddleware(object):
    """Load data about the currently-logged-in Facebook app user."""

    def process_request(self, request):
        # Exit early if we are not in the Facebook app section of the site to
        # avoid clashing with the Django auth middleware.
        if not in_facebook_app(request):
            return None

        # Default to an anonymous user.
        request.user = AnonymousFacebookUser()
        locale = None
        try:
            user = FacebookUser.objects.get(id=request.session[SESSION_KEY])
            request.user = user
            locale = user.locale
        except (FacebookUser.DoesNotExist, KeyError):
            pass

        if locale is None:
            # Since we can't get their locale from their user data, we'll use
            # funfactory's prefixer instead.
            prefixer = Prefixer(request)
            locale = prefixer.get_language()

        activate_locale(request, locale)
