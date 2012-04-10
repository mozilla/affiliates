import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_control

import jingo
from babel.dates import get_month_names
from babel.numbers import format_number

from badges.models import (Badge, BadgeInstance, Category, ClickStats,
                           Leaderboard, Subcategory)
from news.models import NewsItem
from shared.decorators import login_required
from shared.utils import current_locale, redirect


@login_required
def new_badge_step1(request):
    """Display groups of badges available to the user."""
    categories = Category.objects.filter(subcategory__badge__displayed=True).distinct()

    return dashboard(request, 'badges/new_badge/step1.html',
                     {'categories': categories})


@login_required
def new_badge_step2(request, subcategory_pk):
    """Display a set of badges for the user to choose from."""
    subcategory = get_object_or_404(Subcategory, pk=subcategory_pk)
    badges = get_list_or_404(Badge, subcategory=subcategory, displayed=True)

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
