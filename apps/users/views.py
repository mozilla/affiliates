import jingo

from affiliates.views import home
from users.forms import RegisterForm
from users.models import RegisterProfile


def register(request):
    """Create a registration profile."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
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


def activate(request):
    """Activate a registration profile and create a user."""
    pass
