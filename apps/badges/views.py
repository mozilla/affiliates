import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language

import jingo
from babel.core import Locale
from babel.dates import get_month_names
from babel.numbers import format_number
from session_csrf import anonymous_csrf

from badges.models import (Badge, BadgeInstance, Category, ClickStats,
                           Subcategory)
from news.models import NewsItem
from users.forms import RegisterForm, LoginForm


@anonymous_csrf
def home(request, register_form=None, login_form=None):
    """Display the home page."""
    # Redirect logged-in users
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('badges.new.step1'))

    if register_form is None:
        register_form = RegisterForm()
    if login_form is None:
        login_form = LoginForm()

    return jingo.render(request, 'badges/home.html',
                        {'register_form': register_form,
                         'login_form': login_form})


@login_required(redirect_field_name='')
def new_badge_step1(request):
    categories = Category.objects.all()

    return dashboard(request, 'badges/new_badge/step1.html',
                        {'categories': categories})


@login_required(redirect_field_name='')
def new_badge_step2(request, subcategory_pk):
    subcategory = Subcategory.objects.get(pk=subcategory_pk)
    badges = Badge.objects.filter(subcategory=subcategory)

    return dashboard(request, 'badges/new_badge/step2.html',
                        {'subcategory': subcategory, 'badges': badges})


def my_badges(request):
    instance_categories = (BadgeInstance.objects
                           .for_user_by_category(request.user))
    return dashboard(request, 'badges/my_badges.html',
                     {'instance_categories': instance_categories})


@login_required(redirect_field_name='')
def dashboard(request, template, context=None):
    """
    Performs common operations needed by pages using the 'dashboard' template.
    """
    if context is None:
        context = {}

    # Set context variables needed by all dashboard pages
    context['newsitem'] = NewsItem.objects.current()
    context['user_clicks_total'] = format_number(ClickStats.objects
                                    .total(badge_instance__user=request.user))
    context['user_has_created_badges'] = request.user.has_created_badges()

    locale = Locale.parse(get_language(), sep='-')
    month_names_short = get_month_names('abbreviated', locale=locale)
    month_names_full = get_month_names('wide', locale=locale)
    month_names_short_list = [name for k, name in month_names_short.items()]
    month_names_full_list = [name for k, name in month_names_full.items()]

    context['month_names_short'] = month_names_short.items()
    context['month_names_full_list_json'] = json.dumps(month_names_full_list)
    context['month_names_short_list_json'] = json.dumps(month_names_short_list)

    return jingo.render(request, template, context)
