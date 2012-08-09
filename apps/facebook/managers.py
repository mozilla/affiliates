from django.conf import settings
from django.contrib.auth.models import User

from caching.base import CachingManager

from shared.tokens import TokenGenerator


class FacebookUserManager(CachingManager):
    """
    Handles operations involving creating and retrieving users of the Facebook
    app.
    """

    def get_or_create_user_from_decoded_request(self, decoded_request):
        """
        Retrieves the user associated with the decoded request's user_id, or
        return create one if no such user exists. Returns None if the user has
        not authorized the app.
        """
        user_id = decoded_request.get('user_id', None)
        if user_id is None:
            return None, False

        return self.get_or_create(id=user_id)


class FacebookAccountLinkManager(CachingManager):
    def get_token_generator(self, link):
        return TokenGenerator(link.generate_token_state,
                              delay=settings.FACEBOOK_LINK_DELAY)

    def create_link(self, facebook_user, affiliates_email):
        """
        Attempts to link a FacebookUser to an Affiliates user account. The link
        has to be confirmed via a link in the verification email before it is
        finalized.
        """
        try:
            affiliates_user = User.objects.get(email=affiliates_email)
        except User.DoesNotExist:
            return False

        try:
            link = self.get(facebook_user=facebook_user)
        except self.model.DoesNotExist:
            link = self.model(facebook_user=facebook_user)
        link.affiliates_user = affiliates_user

        # Exit early if an active link already exists.
        if link.is_active:
            return False

        # Even if the link is old, generate a fresh activation code.
        token_generator = self.get_token_generator(link)
        link.activation_code = token_generator.generate_token()
        link.save()
        return link
