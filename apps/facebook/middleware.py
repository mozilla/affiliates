from facebook.auth import SESSION_KEY
from facebook.models import FacebookUser


class FacebookAuthenticationMiddleware(object):
    """Load data about the currently-logged-in Facebook app user."""

    def process_request(self, request):
        if SESSION_KEY in request.session:
            try:
                user = FacebookUser.objects.get(id=request.session[SESSION_KEY])
            except FacebookUser.DoesNotExist:
                return None
            request.user = user
