import hashlib
import json
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.utils.translation import get_language
from django.views.decorators.http import require_POST

from django_browserid import get_audience, verify as verify_assertion
from funfactory.urlresolvers import reverse

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

    audience = get_audience(request)
    verification = verify_assertion(assertion, audience)
    if not verification:
        return HttpResponseForbidden()

    response_data = {'registered': False}
    try:
        user = authenticate(assertion=assertion, audience=audience)
        if user is not None:
            login(request, user)
            response_data = {'registered': True,
                             'redirect': reverse('my_badges')}
    except User.MultipleObjectsReturned:
        log.error('Multiple users found for email: %s' % verification['email'])
    except User.DoesNotExist:
        pass

    return HttpResponse(json.dumps(response_data),
                        mimetype='application/json')


@require_POST
def register(request, form):
    """Register a BrowserID-authed user with Affiliates."""
    if form.is_valid():
        assertion = form.cleaned_data['assertion']
        audience = get_audience(request)
        verification = verify_assertion(assertion, audience)
        if not verification:
            return

        # Check if user exists (and auth if they do)
        user = authenticate(assertion=assertion, audience=audience)
        if user is None:
            email = verification['email']
            username = hashlib.sha1(email).hexdigest()[:30]
            display_name = form.cleaned_data['display_name']

            user = User.objects.create_user(username, email)
            user.is_active = True;
            user.save()

            UserProfile.objects.create(user=user, display_name=display_name,
                                       locale=get_language().lower())

            # New user must be authenticated to log in
            user = authenticate(assertion=assertion, audience=audience)


        login(request, user)

        return redirect('my_badges')
