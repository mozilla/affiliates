import hashlib
import json
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.utils.translation import get_language
from django.views.decorators.http import require_POST

from funfactory.urlresolvers import reverse

from browserid.utils import verify as browserid_verify
from shared.utils import redirect
from users.models import UserProfile


log = logging.getLogger('a.browserid')


@require_POST
def verify(request):
    """
    Verify a BrowserID assertion, and return whether a user is registered
    with Affiliates.
    """
    assertion = request.POST.get('assertion', None)
    if assertion is None:
        return HttpResponseBadRequest()

    verification = browserid_verify(request, assertion)
    if not verification:
        return HttpResponseForbidden()

    response_data = {'registered': False}
    user = authenticate(request=request)
    if user is not None:
        login(request, user)
        response_data = {'registered': True, 'redirect': reverse('my_badges')}

    return HttpResponse(json.dumps(response_data),
                        mimetype='application/json')


@require_POST
def register(request, form):
    """Register a BrowserID-authed user with Affiliates.

    Not hooked up to a urlconf; called by other views.
    """
    if form.is_valid():
        verification = browserid_verify(request)
        if not verification:
            return None

        # Check if user exists (and auth if they do)
        user = authenticate(request=request)
        if user is None:
            email = verification['email']
            username = hashlib.sha1(email).hexdigest()[:30]
            display_name = form.cleaned_data['display_name']

            user = User.objects.create_user(username, email)
            user.is_active = True;
            user.save()

            UserProfile.objects.create(user=user, display_name=display_name)

            # New user must be authenticated to log in
            user = authenticate(request=request)
        login(request, user)
        return redirect('my_badges')
    return None
