import jingo

from users.forms import RegisterForm


def home(request, register_form=None):
    """Display the home page."""
    if register_form is None:
        register_form = RegisterForm()

    return jingo.render(request, 'affiliates/home.html',
                        {'register_form': register_form})
