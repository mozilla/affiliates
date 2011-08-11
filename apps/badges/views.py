from django.core.urlresolvers import get_callable

import jingo
from session_csrf import anonymous_csrf

from badges.models import Badge, Category, Subcategory
from users.forms import RegisterForm


@anonymous_csrf
def home(request, register_form=None):
    """Display the home page."""
    if not register_form:
        register_form = RegisterForm()

    return jingo.render(request, 'badges/home.html',
                        {'register_form': register_form})


def new_badge_step1(request):
    categories = Category.objects.all()

    return jingo.render(request, 'badges/new_badge/step1.html',
                        {'categories': categories})


def new_badge_step2(request):
    subcategory_pk = request.GET.get('subcategory')
    subcategory = Subcategory.objects.get(pk=subcategory_pk)
    badges = Badge.objects.all_from_subcategory(subcategory)

    return jingo.render(request, 'badges/new_badge/step2.html',
                        {'subcategory': subcategory, 'badges': badges})


def new_badge_step3(request):
    badge_class, pk = Badge.objects.from_badge_str(request.GET.get('badge'))
    customize_view = get_callable(badge_class.customize_view)
    return customize_view(request, pk=pk)
