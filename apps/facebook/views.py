from django import http
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect as django_redirect
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import basket
import commonware
import jingo
from commonware.response.decorators import xframe_allow
from funfactory.urlresolvers import reverse
from tower import ugettext as _

from facebook.auth import login
from facebook.decorators import fb_login_required
from facebook.forms import (FacebookAccountLinkForm, FacebookBannerInstanceForm,
                            LeaderboardFilterForm, NewsletterSubscriptionForm)
from facebook.tasks import add_click, generate_banner_instance_image
from facebook.models import (FacebookAccountLink, FacebookBannerInstance,
                             FacebookClickStats, FacebookUser)
from facebook.utils import activate_locale, decode_signed_request, is_logged_in
from shared.http import JSONResponse
from shared.utils import absolutify, redirect


log = commonware.log.getLogger('a.facebook')


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

    # Attach country data to the user object. This can only be retrieved from
    # the decoded request, so we add it here and login saves it.
    user.country = decoded_request['user']['country']

    # User has been authed, let's log them in.
    login(request, user)

    # Normally the FacebookAuthenticationMiddleware activates the locale for
    # the user, but since it does not run for this view, we need to activate it
    # manually.
    activate_locale(request, user.locale)

    if user.is_new:
        return jingo.render(request, 'facebook/first_run.html')

    # TODO: Replace with actual app landing page.
    return banner_list(request)


@fb_login_required
@xframe_allow
def banner_create(request):
    form = FacebookBannerInstanceForm(request, request.POST or None)
    if request.method == 'POST':
        if not form.is_valid():
            return JSONResponse(form.errors, status=400)

        banner_instance = form.save(commit=False)
        banner_instance.user = request.user
        banner_instance.save()

        # The create form is submitted via an AJAX call. If the user wants to
        # include their profile picture on a banner, we return a 202 Accepted to
        # indicate we are processing the image. If they don't, we just return
        # a 201 Created to signify that the banner instance has been created
        # and it is safe to continue.
        if request.POST['next_action'] == 'share':
            next = absolutify(reverse('facebook.banners.share',
                                      args=[banner_instance.id]))
        else:
            next = absolutify(reverse('facebook.banner_list'))

        if form.cleaned_data['use_profile_image']:
            generate_banner_instance_image.delay(banner_instance.id)

            payload = {
                'check_url': reverse('facebook.banners.create_image_check',
                                     args=[banner_instance.id]),
                'next': next
            }
            return JSONResponse(payload, status=202)  # 202 Accepted
        else:
            # No processing needed.
            banner_instance.processed = True
            banner_instance.save()
            return JSONResponse({'next': next}, status=201)  # 201 Created

    return jingo.render(request, 'facebook/banner_create.html', {'form': form})


@fb_login_required
@never_cache
def banner_create_image_check(request, instance_id):
    """Check the status of generating a custom image for a banner instance."""
    banner_instance = get_object_or_404(FacebookBannerInstance, id=instance_id)
    return JSONResponse({'is_processed': banner_instance.processed})


@fb_login_required
@xframe_allow
def banner_list(request):
    banner_instances = request.user.banner_instance_set.filter(processed=True)
    return jingo.render(request, 'facebook/banner_list.html',
                        {'banner_instances': banner_instances})


@fb_login_required
@xframe_allow
def banner_share(request, instance_id):
    banner_instance = get_object_or_404(FacebookBannerInstance, id=instance_id,
                                        user=request.user)
    protocol = 'https' if request.is_secure() else 'http'
    next = absolutify(reverse('facebook.post_banner_share'),
                              protocol=protocol)
    return jingo.render(request, 'facebook/banner_share.html',
                        {'banner_instance': banner_instance, 'next': next})


def post_banner_share(request):
    """
    Redirect user back to the app after they've posted a banner to their feed.
    """
    messages.success(request, _('You have successfully posted a banner to your '
                                'wall !'))
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
    form = LeaderboardFilterForm(request.GET or None)
    top_users = form.get_top_users()
    return jingo.render(request, 'facebook/leaderboard.html',
                        {'top_users': top_users, 'form': form})


@fb_login_required
@xframe_allow
def invite(request):
    protocol = 'https' if request.is_secure() else 'http'
    next = absolutify(reverse('facebook.post_invite'), protocol=protocol)
    return jingo.render(request, 'facebook/invite.html', {'next': next})


def post_invite(request):
    """
    Redirect user back to the app after they've invited friends to download
    Firefox.
    """
    messages.success(request, _('You have successfully sent a message to one '
                                'of your friends!'))
    return django_redirect(settings.FACEBOOK_APP_URL)


@fb_login_required
@require_POST
def newsletter_subscribe(request):
    form = NewsletterSubscriptionForm(request.user, request.POST)
    if form.is_valid():
        data = form.cleaned_data
        try:
            basket.subscribe(data['email'], settings.FACEBOOK_MAILING_LIST,
                             format=data['format'], country=data['country'])
        except basket.BasketException, e:
            log.error('Error subscribing email %s to mailing list: %s' %
                      (data['email'], e))

    # TODO: Send an error code if there was an error.
    return JSONResponse({'success': 'success'})


@fb_login_required
@cache_control(must_revalidate=True, max_age=3600)
def stats(request, year, month):
    """
    Returns statistics for the sidebar statistics display. Called via AJAX.
    """
    # Use `or 0` in case of None result.
    clicks = (FacebookClickStats.objects
              .filter(banner_instance__user=request.user)
              .filter(hour__month=month, hour__year=year)
              .aggregate(Sum('clicks'))['clicks__sum']) or 0
    return JSONResponse({'clicks': clicks})
