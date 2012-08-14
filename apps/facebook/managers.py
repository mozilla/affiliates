from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

import jingo
from caching.base import CachingManager
from tower import ugettext as _

from shared.tokens import TokenGenerator
from shared.utils import get_object_or_none


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
        affiliates_user = get_object_or_none(User, email=affiliates_email)
        if affiliates_user is None:
            return False

        # Exit early if the affiliates user already has an active account link.
        if affiliates_user.account_links.filter(is_active=True).exists():
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

    def send_activation_email(self, request, link):
        """
        Send an email to an Affiliates user to confirm that they consent to
        linking their account with a Facebook account.
        """
        subject = _('Link your Firefox Affiliates account')
        message = jingo.render_to_string(request,
                                         'facebook/link_activation_email.html',
                                         {'link': link})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  [link.affiliates_user.email])

    def activate_link(self, activation_code):
        """Verify activation code and activate the corresponding link."""
        link = get_object_or_none(self.model, activation_code=activation_code)
        if link is None or link.is_active:
            return None

        token_generator = self.get_token_generator(link)
        if not token_generator.verify_token(activation_code):
            return None

        link.is_active = True
        link.save()
        return link
