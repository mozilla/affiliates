from users.forms import ActivationForm


def activation_form_defaults():
    """Returns a set of default values for testing the activation form."""
    return {'username': 'TestUser', 'password': 'asdfasdf',
            'password2': 'asdfasdf', 'name': 'Test User',
            'email': 'test@user.com', 'country': 'us',
            'locale': 'en-US', 'accept_email': True}


def activation_form(**kwargs):
    """Return an activation form with default values"""
    defaults = activation_form_defaults()
    defaults.update(kwargs)

    return ActivationForm(defaults)
