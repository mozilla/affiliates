import jingo
from session_csrf import anonymous_csrf

from users.forms import RegisterForm

@anonymous_csrf
def home(request, register_form=None):
    """Display the home page."""
    if not register_form:
        register_form = RegisterForm()

    return jingo.render(request, 'badges/home.html',
                        {'register_form': register_form})
