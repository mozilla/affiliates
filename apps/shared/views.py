from django.conf import settings
from django.shortcuts import render
from django.utils.http import urlquote_plus
from django.utils.translation import get_language
from django.views.decorators.http import require_POST
from django.views.defaults import page_not_found, server_error

import basket
import commonware
from funfactory.urlresolvers import reverse
from session_csrf import anonymous_csrf
from tower import ugettext_lazy as _lazy

from badges.views import dashboard
from browserid.forms import RegisterForm as BrowserIDRegisterForm
from browserid.views import register as browserid_register
from facebook.utils import in_facebook_app
from shared.decorators import login_required
from shared.forms import NewsletterForm
from shared.http import JSONResponse
from shared.utils import absolutify, redirect
from users.forms import RegisterForm, LoginForm


TWEET_TEXT = _lazy(u'The Firefox Affiliates program is a great way to share '
                   'your love of Mozilla Firefox.')
BROWSERID_NO_ASSERTION = _lazy(u'There was an error during authentication. '
                               'Please try again.')
BROWSERID_VERIFY_FAIL = _lazy(u'BrowserID could not verify your identity. '
                              'Visit <a href="{url}">browserid.org</a> for '
                              'more information.')


log = commonware.log.getLogger('a.shared')


@anonymous_csrf
def home(request, register_form=None, login_form=None):
    """Display the home page."""
    # Redirect logged-in users
    if request.user.is_authenticated():
        return redirect('badges.new.step1')

    # en-US users see the BrowserID view instead
    if get_language() in settings.BROWSERID_LOCALES:
        return browserid_home(request)

    if register_form is None:
        register_form = RegisterForm()
    if login_form is None:
        login_form = LoginForm()

    params = {'register_form': register_form,
              'login_form': login_form,
              'share_url': absolutify('/', protocol='https'),
              'tweet_text': urlquote_plus(TWEET_TEXT)}
    return render(request, 'shared/home/normal.html', params)


def browserid_home(request):
    """Display the home page with a BrowserID login."""
    register_form = BrowserIDRegisterForm(request.POST or None)
    if request.method == 'POST':
        # Attempting to register
        response = browserid_register(request, register_form)
        if response is not None:
            return response

    params = {'browserid_verify': reverse('browserid.verify'),
              'register_form': register_form,
              'share_url': absolutify('/', protocol='https'),
              'tweet_text': urlquote_plus(TWEET_TEXT),
              'browserid_no_assertion': BROWSERID_NO_ASSERTION,
              'browserid_verify_fail': BROWSERID_VERIFY_FAIL}
    return render(request, 'shared/home/browserid.html', params)


@login_required
def about(request):
    return dashboard(request, 'shared/about.html')


@login_required
def faq(request):
    return dashboard(request, 'shared/faq.html')


def view_404(request):
    template = '404.html'
    if in_facebook_app(request):
        template = 'facebook/error.html'

    return render(request, template, status=404)


def view_500(request):
    if in_facebook_app(request):
        return render(request, 'facebook/error.html', status=500)
    else:
        return server_error(request)


@login_required
@require_POST
def newsletter_subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        try:
            basket.subscribe(form.cleaned_data['email'],
                             settings.BASKET_NEWSLETTER,
                             source_url=request.build_absolute_uri())
        except basket.BasketException, e:
            log.error('Error subscribing email %s to mailing list: %s' %
                      (form.cleaned_data['email'], e))

    return JSONResponse({'success': 'success'})
