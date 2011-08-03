import jingo

from users.forms import RegisterForm


def home(request, register_form=None):
    """Display the home page."""
    if not register_form:
        register_form = RegisterForm()

    return jingo.render(request, 'badges/home.html',
                        {'register_form': register_form})
