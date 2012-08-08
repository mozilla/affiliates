import base64

from django.conf import settings

import jingo
from mock import patch

from facebook.auth import SESSION_KEY
from facebook.models import FacebookUser
from facebook.tests import create_payload
from facebook.utils import in_facebook_app
from facebook.views import load_app


class FacebookAuthenticationMiddleware(object):
    """Load data about the currently-logged-in Facebook app user."""

    def process_request(self, request):
        # Exit early if we are not in the Facebook app section of the site to
        # avoid clashing with the Django auth middleware.
        if not in_facebook_app(request):
            return None

        if SESSION_KEY in request.session:
            try:
                user = FacebookUser.objects.get(id=request.session[SESSION_KEY])
            except FacebookUser.DoesNotExist:
                return None
            request.user = user


class FacebookDebugMiddleware(object):
    """
    If FACEBOOK_DEBUG is True, this middleware changes the Facebook app
    parts of the site to be displayed in an iframe and auto-auths the user as
    the Facebook user with the ID specified in settings.FACEBOOK_DEBUG_USER_ID.
    """
    def __init__(self):
        self.decode_patcher = None

        # Mock out CSP_FRAME_SRC to allow data URI in iframe.
        new_csp_frame_src = list(settings.CSP_FRAME_SRC) + ['data:']
        self.csp_patcher = patch.object(settings, 'CSP_FRAME_SRC',
                                        new_csp_frame_src)

    def process_request(self, request):
        self.is_active = (getattr(settings, 'FACEBOOK_DEBUG', False) and
                          in_facebook_app(request))

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Mock in signed_request if user is viewing the login view."""
        if not self.is_active:
            return None

        self.csp_patcher.start()

        user_id = getattr(settings, 'FACEBOOK_DEBUG_USER_ID', None)
        if view_func == load_app and user_id:
            request.method = 'POST'
            post = request.POST.copy()
            post['signed_request'] = 'signed_request'
            request.POST = post

            self.decode_patcher = patch('facebook.views.decode_signed_request')
            decode_mock = self.decode_patcher.start()
            decode_mock.return_value = create_payload(user_id=user_id)

    def process_response(self, request, response):
        """Add an iframe wrapper and deactivate decode patch."""
        if not self.is_active:
            return response

        # Disable CSP patcher as it has already been added to the response by
        # now.
        self.csp_patcher.stop()

        if self.decode_patcher is not None:
            self.decode_patcher.stop()

        # Use a base64 data URI to shove the response content into an iframe.
        template = jingo.env.get_template('facebook/debug_wrapper.html')
        content = base64.b64encode(response.content)
        response.content = template.render(content=content)
        return response
