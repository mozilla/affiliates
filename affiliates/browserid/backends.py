from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from affiliates.browserid.utils import verify


class BrowserIDSessionBackend(ModelBackend):
    """
    Auth backend that stores a BrowserID verification in the user's session.
    """
    def authenticate(self, request=None, assertion=None):
        if request:
            verification = verify(request, assertion)
            if not verification:
                return None

            try:
                user = User.objects.get(email=verification['email'])
                if user.is_active:
                    return user
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass

        return None
