from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import jingo
from session_csrf import anonymous_csrf

from badges.models import Badge, BadgeInstance, Category, Subcategory
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


def dashboard(request, template, context=None):
    """
    Performs common operations needed by pages using the 'dashboard' template.
    """
    if context is None:
        context = {}

    context['newsitem'] = NewsItem.objects.current()

    return jingo.render(request, template, context)
