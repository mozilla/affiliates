from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import get_callable, reverse
from django.http import HttpResponseRedirect

import jingo
from session_csrf import anonymous_csrf

from badges.models import Badge, Category, Subcategory
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

    return jingo.render(request, 'badges/new_badge/step1.html',
                        {'categories': categories})


@login_required(redirect_field_name='')
def new_badge_step2(request):
    subcategory_pk = request.GET.get('subcategory')
    subcategory = Subcategory.objects.get(pk=subcategory_pk)
    badges = Badge.objects.all_from_subcategory(subcategory)

    return jingo.render(request, 'badges/new_badge/step2.html',
                        {'subcategory': subcategory, 'badges': badges})


@login_required(redirect_field_name='')
def new_badge_step3(request):
    badge_class, pk = Badge.objects.from_badge_str(request.GET.get('badge'))
    customize_view = get_callable(badge_class.customize_view)
    return customize_view(request, pk=pk)
