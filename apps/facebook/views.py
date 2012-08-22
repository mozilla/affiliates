from django import http
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect as django_redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import jingo
from commonware.response.decorators import xframe_allow
from funfactory.urlresolvers import reverse

from facebook.auth import login
from facebook.decorators import fb_login_required
from facebook.forms import FacebookAccountLinkForm, FacebookBannerInstanceForm
from facebook.tasks import add_click, generate_banner_instance_image
from facebook.models import (FacebookAccountLink, FacebookBannerInstance,
                             FacebookUser)
from facebook.utils import decode_signed_request, is_logged_in
from shared.http import JSONResponse
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
def banner_create(request):
    form = FacebookBannerInstanceForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        banner_instance = form.save(commit=False)
        banner_instance.user = request.user
        banner_instance.save()

        # The create form is submitted via an AJAX call. If the user wants to
        # include their profile picture on a banner, we return a 202 Accepted to
        # indicate we are processing the image. If they don't, we just return
        # a 201 Created to signify that the banner instance has been created
        # and it is safe to continue.
        if form.cleaned_data['use_profile_image']:
            generate_banner_instance_image.delay(banner_instance.id)
            payload = {
                'check_url': reverse('facebook.banners.create_image_check',
                                     args=[banner_instance.id]),
                'next': absolutify(reverse('facebook.banner_list'))
            }
            return JSONResponse(payload, status=202)  # 202 Accepted
        else:
            payload = {'next': absolutify(reverse('facebook.banner_list'))}
            return JSONResponse(payload, status=201)  # 201 Created

    return jingo.render(request, 'facebook/banner_create.html', {'form': form})


@fb_login_required
@never_cache
def banner_create_image_check(request, instance_id):
    """Check the status of generating a custom image for a banner instance."""
    banner_instance = get_object_or_404(FacebookBannerInstance, id=instance_id)
    is_complete = bool(banner_instance.custom_image)
    return JSONResponse({'is_complete': is_complete})


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


def activate_link(request, activation_code):
    link = FacebookAccountLink.objects.activate_link(activation_code)
    if link:
        return django_redirect(settings.FACEBOOK_APP_URL)
    else:
        raise http.Http404


@fb_login_required
@xframe_allow
@require_POST
def remove_link(request):
    link = get_object_or_404(FacebookAccountLink, facebook_user=request.user)
    link.delete()
    return banner_list(request)


def follow_banner_link(request, banner_instance_id):
    """
    Add a click to a banner instance and redirect the user to the Firefox
    download page.
    """
    add_click.delay(banner_instance_id)
    return django_redirect(settings.FACEBOOK_DOWNLOAD_URL)


@fb_login_required
@xframe_allow
def leaderboard(request):
    top_users = FacebookUser.objects.order_by('leaderboard_position')[:25]
    return jingo.render(request, 'facebook/leaderboard.html',
                        {'top_users': top_users})
