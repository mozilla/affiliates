import json
from urllib import quote_plus

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.translation import get_language

import jingo
from babel.core import Locale
from babel.dates import get_month_names
from babel.numbers import format_number
from session_csrf import anonymous_csrf
from tower import ugettext_lazy as _lazy

from badges.models import (Badge, BadgeInstance, Category, ClickStats,
                           Leaderboard, Subcategory)
from news.models import NewsItem
from shared.decorators import login_required
from shared.utils import absolutify, redirect
from users.forms import RegisterForm, LoginForm


TWEET_TEXT = _lazy(u'The Firefox Affiliates program is a great way to share '
                   'your love of Mozilla Firefox.')


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
              'tweet_text': quote_plus(TWEET_TEXT)}
    return jingo.render(request, 'badges/home.html', params)


@login_required
def new_badge_step1(request):
    categories = Category.objects.all()

    return dashboard(request, 'badges/new_badge/step1.html',
                        {'categories': categories})


@login_required
def new_badge_step2(request, subcategory_pk):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_pk)
    badges = Badge.objects.filter(subcategory=subcategory)

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

    locale = Locale.parse(get_language(), sep='-')

    # Set context variables needed by all dashboard pages
    context['newsitem'] = NewsItem.objects.current()
    context['user_has_created_badges'] = request.user.has_created_badges()

    if context['user_has_created_badges']:
        clicks_total = (ClickStats.objects
                        .total(badge_instance__user=request.user))
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
def month_stats_ajax(request):
    user_total = ClickStats.objects.total(badge_instance__user=request.user,
                                          month=request.POST['month'],
                                          year=request.POST['year'])
    site_avg = ClickStats.objects.average_for_period(month=request.POST['month'],
                                                     year=request.POST['year'])

    locale = Locale.parse(get_language(), sep='-')
    results = {'user_total': format_number(user_total, locale=locale),
               'site_avg': format_number(site_avg, locale=locale)}
    return HttpResponse(json.dumps(results), mimetype='application/json')
