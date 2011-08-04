from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import jingo

from badges.views import home
from users.forms import ActivationForm, RegisterForm
from users.models import RegisterProfile


def register(request):
    """Create a registration profile."""
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # Create a registration profile, which also emails
        # activation details
        profile = RegisterProfile.objects.create_profile(
            form.cleaned_data['name'], form.cleaned_data['email'],
            form.cleaned_data['password'])

        return jingo.render(request, 'users/register_done.html',
                            {'profile': profile})
    else:
        form = RegisterForm()

    return home(request, register_form=form)


def activate(request, activation_key=None):
    """Activate a registration profile and create a user."""

    # Invalid keys get booted to the homepage
    reg_profile = RegisterProfile.objects.get_by_key(activation_key)
    if (reg_profile is None):
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = ActivationForm(request.POST)
        user = RegisterProfile.objects.activate_profile(activation_key, form)
        if user:
            return jingo.render(request, 'users/activate_done.html',
                                {'user': user})
    else:
        form = ActivationForm(initial={'name': reg_profile.name,
                                       'email': reg_profile.email})

    params = {'form': form, 'activation_key': activation_key}
    return jingo.render(request, 'users/activate.html', params)
