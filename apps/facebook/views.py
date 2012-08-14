from django import http
from django.conf import settings
from django.shortcuts import redirect as django_redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import jingo
from commonware.response.decorators import xframe_allow
from funfactory.urlresolvers import reverse

from facebook.auth import login
from facebook.decorators import fb_login_required
from facebook.forms import FacebookAccountLinkForm, FacebookBannerInstanceForm
from facebook.models import FacebookAccountLink, FacebookUser
from facebook.utils import decode_signed_request, is_logged_in
from shared.utils import absolutify, redirect


@require_POST
@csrf_exempt
@xframe_allow
def load_app(request):
    """
    Create or authenticate the Facebook user and direct them to the correct
    area of the app upon their entry.
    """
    signed_request = request.POST.get('signed_request', None)
    if signed_request is None:
        # App wasn't loaded within a canvas, redirect to the home page.
        return redirect('home')

    decoded_request = decode_signed_request(signed_request,
                                            settings.FACEBOOK_APP_SECRET)
    if decoded_request is None:
        return redirect('home')

    user, created = (FacebookUser.objects.
            get_or_create_user_from_decoded_request(decoded_request))
    if user is None:
        # User has yet to authorize the app, offer authorization.
        context = {
            'app_id': settings.FACEBOOK_APP_ID,
            'app_namespace': settings.FACEBOOK_APP_NAMESPACE,
            'app_permissions': settings.FACEBOOK_PERMISSIONS
        }
        return jingo.render(request, 'facebook/oauth_redirect.html', context)

    # User has been authed, let's log them in.
    login(request, user)

    if user.is_new:
        return jingo.render(request, 'facebook/first_run.html')

    # TODO: Replace with actual app landing page.
    return banner_list(request)


@fb_login_required
@xframe_allow
def create_banner(request):
    form = FacebookBannerInstanceForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        banner_instance = form.save(commit=False)
        banner_instance.user = request.user
        banner_instance.save()
        return banner_list(request)

    return jingo.render(request, 'facebook/create_banner.html', {'form': form})


@fb_login_required
@xframe_allow
def banner_list(request):
    banner_instances = request.user.banner_instance_set.all()
    protocol = 'https' if request.is_secure() else 'http'
    share_banner_redirect = absolutify(reverse('facebook.post_banner_share'),
                                       protocol=protocol)
    ctx = {'banner_instances': banner_instances,
           'share_banner_redirect': share_banner_redirect}
    return jingo.render(request, 'facebook/banner_list.html', ctx)


def post_banner_share(request):
    """
    Redirect user back to the app after they've posted a banner to their feed.
    """
    return django_redirect(settings.FACEBOOK_APP_URL)


@require_POST
def link_accounts(request):
    """
    Link the current user's account with an Affiliates account. Called via AJAX
    by the frontend.
    """
    if not is_logged_in(request):
        # Only logged in users can link accounts.
        return http.HttpResponseForbidden()

    form = FacebookAccountLinkForm(request.POST or None)
    if form.is_valid():
        affiliates_email = form.cleaned_data['affiliates_email']
        link = FacebookAccountLink.objects.create_link(request.user,
                                                       affiliates_email)
        if link:
            FacebookAccountLink.objects.send_activation_email(request, link)

    # Tell the user we were successful regardless of outcome in order to avoid
    # revealing valid emails.
    return http.HttpResponse()
