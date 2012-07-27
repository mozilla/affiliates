from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import jingo
from commonware.response.decorators import xframe_allow

from facebook.auth import login
from facebook.decorators import fb_login_required
from facebook.forms import FacebookBannerInstanceForm
from facebook.models import FacebookUser
from facebook.utils import decode_signed_request
from shared.utils import redirect


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
    form = FacebookBannerInstanceForm(request.POST or None)
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
    return jingo.render(request, 'facebook/banner_list.html',
                        {'banner_instances': banner_instances})
