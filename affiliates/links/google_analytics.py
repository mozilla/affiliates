import httplib2

from django.conf import settings

from apiclient.discovery import build as build_service
from apiclient.errors import HttpError
from oauth2client.client import Error as OAuth2Error, SignedJwtAssertionCredentials


class AnalyticsError(Exception):
    pass


class AnalyticsService(object):
    """
    Handles connecting to the Google Analytics API and retrieving data
    about banner referrals.
    """
    def __init__(self, keyfile=None, email=None, profile_id=None):
        """
        :param keyfile:
            Path to the PKCS 12 file for authenticating with the API as
            a service account. Defaults to settings.GA_API_KEYFILE.

        :param email:
            Email address for the service account to authenticate as.
            Defaults to settings.GA_API_ACCOUNT_EMAIL.

        :param profile_id:
            ID of analytics profile to query. Defaults to
            settings.GA_API_PROFILE_ID.
        """
        self.profile_id = profile_id or settings.GA_API_PROFILE_ID
        keyfile = keyfile or settings.GA_API_KEYFILE

        try:
            with open(keyfile, 'rb') as f:
                key = f.read()
        except IOError as e:
            raise AnalyticsError('Could not read keyfile `{0}`: {1}'.format(keyfile, e), e)

        email = email or settings.GA_API_ACCOUNT_EMAIL
        credentials = SignedJwtAssertionCredentials(
            email, key, scope='https://www.googleapis.com/auth/analytics.readonly')
        http = httplib2.Http()
        http = credentials.authorize(http)

        try:
            self._service = build_service('analytics', 'v3', http=http)
        except OAuth2Error as e:
            raise AnalyticsError('Error authenticating with Analytics API: {0}'.format(e), e)

    def _get_data(self, **kwargs):
        ga_data = self._service.data().ga()
        query = ga_data.get(ids='ga:{0}'.format(self.profile_id), **kwargs)
        try:
            return query.execute()
        except HttpError as e:
            raise AnalyticsError('Error during HTTP request to API: {0}'.format(e), e)

    def get_clicks_for_date(self, query_date):
        """
        Retrive click totals for all banners that occurred on the given
        date.
        """
        date_string = query_date.strftime('%Y-%m-%d')
        result = self._get_data(
            start_date=date_string,
            end_date=date_string,
            metrics='ga:pageviews',
            dimensions='ga:customVarValue1'
        )

        # We're expecting only unsampled data when not in debug mode.
        if result['containsSampledData'] and not settings.DEBUG:
            raise AnalyticsError('API response contains sampled data when unsampled data was '
                                 'expected.')

        if 'rows' in result:
            return dict(result['rows'])
        else:
            return {}
