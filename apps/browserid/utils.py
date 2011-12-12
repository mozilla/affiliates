from django_browserid import get_audience, verify as browserid_verify


SESSION_VERIFY = 'browserid_verification'


def verify(request, assertion=None):
    """Verifies a BrowserID assertion and caches it in the user's session."""
    if assertion:
        verification = browserid_verify(assertion, get_audience(request))
        request.session[SESSION_VERIFY] = verification
    else:
        verification = request.session.get(SESSION_VERIFY)

    return verification or None
