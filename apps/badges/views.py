import json

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.http import urlquote_plus
from django.views.decorators.cache import cache_control

import jingo
from babel.dates import get_month_names
from babel.numbers import format_number
from session_csrf import anonymous_csrf
from tower import ugettext_lazy as _lazy

from badges.models import (Badge, BadgeInstance, Category, ClickStats,
                           Leaderboard, Subcategory)
from news.models import NewsItem
from shared.decorators import login_required
from shared.utils import absolutify, current_locale, redirect
from users.forms import RegisterForm, LoginForm


TWEET_TEXT = _lazy(u'The Firefox Affiliates program is a great way to share '
                   'your love of Mozilla Firefox.')


CACHE_SUBCAT_MAP = 'subcategory_map_%s'  # %s = locale


@anonymous_csrf
def home(request, register_form=None, login_form=None):
    """Display the home page."""
    # Redirect logged-in users
    if request.user.is_authenticated():
        return redirect('badges.new.step1')

    if register_form is None:
        register_form = RegisterForm()
    if login_form is None:
        login_form = LoginForm()

    params = {'register_form': register_form,
              'login_form': login_form,
              'share_url': absolutify('/'),
              'tweet_text': urlquote_plus(TWEET_TEXT)}
    return jingo.render(request, 'badges/home.html', params)


@login_required
def new_badge_step1(request):
    """Display groups of badges available to the user."""
    user_locale = request.user.userprofile.locale

    categories = Category.objects.all()

    # We don't want to display empty subcategories or categories, so we
    # query each set manually to check for badges available in the user's
    # locale.
    key = CACHE_SUBCAT_MAP % user_locale
    subcategory_map = cache.get(key)
    if subcategory_map is None:
        subcategory_map = {}

        for category in categories:
            subcategories = category.subcategory_set.in_locale(user_locale)
            if subcategories:
                subcategory_map[category.pk] = subcategories

            cache.set(key, subcategory_map)

    return dashboard(request, 'badges/new_badge/step1.html',
                        {'categories': categories,
                         'subcategory_map': subcategory_map})


@login_required
def new_badge_step2(request, subcategory_pk):
    """Display a set of badges for the user to choose from."""
    user_locale = request.user.userprofile.locale

    subcategory = get_object_or_404(Subcategory, pk=subcategory_pk)
    badges = get_list_or_404(Badge, subcategory=subcategory,
                             badgelocale__locale=user_locale)

    return dashboard(request, 'badges/new_badge/step2.html',
                        {'subcategory': subcategory, 'badges': badges})


@login_required
def my_badges(request):
    # New users are redirected to the badge generator
    if not request.user.has_created_badges():
        return redirect('badges.new.step1')

    instance_categories = (BadgeInstance.objects
                           .for_user_by_category(request.user))
    return dashboard(request, 'badges/my_badges.html',
                     {'instance_categories': instance_categories})


@login_required
def dashboard(request, template, context=None):
    """
    Performs common operations needed by pages using the 'dashboard' template.
    """
    if context is None:
        context = {}

    locale = current_locale()

    # Set context variables needed by all dashboard pages
    context['newsitem'] = NewsItem.objects.current()
    context['user_has_created_badges'] = request.user.has_created_badges()

    if context['user_has_created_badges']:
        clicks_total = ClickStats.objects.total_for_user(request.user)
        context['user_clicks_total'] = format_number(clicks_total,
                                                     locale=locale)

        # Statistics Summary
        months_short = get_month_names('abbreviated', locale=locale)
        months_full = get_month_names('wide', locale=locale)
        months_short_list = [name for k, name in months_short.items()]
        months_full_list = [name for k, name in months_full.items()]

        context['months_short'] = months_short.items()
        context['months_full_list_json'] = json.dumps(months_full_list)
        context['months_short_list_json'] = json.dumps(months_short_list)

        # Leaderboard
        try:
            context['show_leaderboard'] = True
            context['leaderboard'] = (Leaderboard.objects
                                      .top_users(settings.LEADERBOARD_SIZE))
            context['user_standing'] = (Leaderboard.objects
                                        .get(user=request.user))
        except Leaderboard.DoesNotExist:
            context['show_leaderboard'] = False

    return jingo.render(request, template, context)


@require_POST
@login_required
@cache_control(must_revalidate=True, max_age=3600)
def month_stats_ajax(request):
    user_total = ClickStats.objects.total_for_user_period(
        request.user, request.POST['month'], request.POST['year'])
    site_avg = ClickStats.objects.average_for_period(
        request.POST['month'], request.POST['year'])

    locale = current_locale()
    results = {'user_total': format_number(user_total, locale=locale),
               'site_avg': format_number(site_avg, locale=locale)}
    return HttpResponse(json.dumps(results), mimetype='application/json')
