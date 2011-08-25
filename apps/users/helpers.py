from jingo import register

from users.models import UserProfile

@register.function
def display_name(user):
    """Return a display name if set, else the username."""
    try:  # Also mostly for tests.
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        return user.username
    return profile.name if profile.name else user.username
