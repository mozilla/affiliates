from caching.base import CachingManager


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
