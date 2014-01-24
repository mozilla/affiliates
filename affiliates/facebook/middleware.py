import base64

from django.conf import settings

import jingo
from funfactory.urlresolvers import Prefixer
from mock import patch

from affiliates.facebook.auth import SESSION_KEY
from affiliates.facebook.models import AnonymousFacebookUser, FacebookUser
from affiliates.facebook.tests import create_payload
from affiliates.facebook.utils import activate_locale, in_facebook_app
from affiliates.facebook.views import load_app


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

        # Mock out decode function for authentication.
        self.decode_patcher = patch('affiliates.facebook.views.decode_signed_request')

    def process_request(self, request):
        request._fb_debug = (getattr(settings, 'FACEBOOK_DEBUG', False) and
                             in_facebook_app(request))

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Mock in signed_request if user is viewing the login view."""
        if not request._fb_debug:
            return None

        # Add patcher to requests to avoid stopping them when they haven't
        # started.
        request.csp_patcher = self.csp_patcher
        request.csp_patcher.start()

        user_id = getattr(settings, 'FACEBOOK_DEBUG_USER_ID', None)
        if view_func == load_app and user_id:
            request.method = 'POST'
            post = request.POST.copy()
            post['signed_request'] = 'signed_request'
            request.POST = post

            request.decode_patcher = self.decode_patcher
            decode_mock = request.decode_patcher.start()
            decode_mock.return_value = create_payload(user_id=user_id)

    def process_response(self, request, response):
        """Add an iframe wrapper and deactivate decode patch."""
        if not request._fb_debug:
            return response

        if getattr(request, 'csp_patcher', False):
            request.csp_patcher.stop()

        if getattr(request, 'decode_patcher', False):
            request.decode_patcher.stop()

        # Use a base64 data URI to shove the response content into an iframe.
        template = jingo.env.get_template('facebook/debug_wrapper.html')
        content = base64.b64encode(response.content)
        response.content = template.render(content=content)
        return response
