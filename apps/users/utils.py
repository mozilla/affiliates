from django.contrib.auth.models import User


def hash_password(raw_password):
    """Generates a hash for the password using the app-specified algorithm."""
    u = User()
    u.set_password(raw_password)
    return u.password
