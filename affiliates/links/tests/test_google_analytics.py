from datetime import date

from mock import ANY, Mock, mock_open, patch
from nose.tools import eq_
from oauth2client.client import Error as OAuth2Error

from affiliates.base.tests import TestCase
from affiliates.links.google_analytics import AnalyticsError, AnalyticsService


class AnalyticsServiceTests(TestCase):
    def setUp(self):
        # Avoid connecting to real API during tests.
        self.build_service = self.create_patch('affiliates.links.google_analytics.build_service')

        with self._mock_open():
            self.service = AnalyticsService('keyfile.p12', 'a@example.com', 125)

    def _mock_open(self, *args, **kwargs):
        m = mock_open(*args, **kwargs)
        return patch('affiliates.links.google_analytics.open', m, create=True)

    def test_init_keyfile_missing(self):
        """If the keyfile can't be found, raise AnalyticsError."""
        with self._mock_open() as _open:
            _open.side_effect = IOError
            with self.assertRaises(AnalyticsError):
                AnalyticsService('keyfile.p12', 'a@example.com', 125)

    def test_init_oauth2error(self):
        """
        If there is an error authenticating via oauth, raise
        AnalyticsError.
        """
        with self._mock_open(read_data='asdf'):
            self.build_service.side_effect = OAuth2Error
            with self.assertRaises(AnalyticsError):
                AnalyticsService('keyfile.p12', 'a@example.com', 125)

    def test_init(self):
        with self._mock_open(read_data='asdf') as _open:
            SignedJwtAssertionCredentials = self.create_patch(
                'affiliates.links.google_analytics.SignedJwtAssertionCredentials')
            credentials = SignedJwtAssertionCredentials.return_value
            http = credentials.authorize.return_value

            service = AnalyticsService('keyfile.p12', 'a@example.com', 125)

            _open.assert_called_with('keyfile.p12', 'rb')
            SignedJwtAssertionCredentials.assert_called_with(
                'a@example.com', 'asdf',
                scope='https://www.googleapis.com/auth/analytics.readonly')
            self.build_service.assert_called_with('analytics', 'v3', http=http)
            eq_(service._service, self.build_service.return_value)
            eq_(service.profile_id, 125)

    def test_init_defaults(self):
        with self._mock_open(read_data='asdf') as _open:
            SignedJwtAssertionCredentials = self.create_patch(
                'affiliates.links.google_analytics.SignedJwtAssertionCredentials')

            with self.settings(GA_API_PROFILE_ID=125, GA_API_KEYFILE='keyfile.p12',
                               GA_API_ACCOUNT_EMAIL='a@example.com'):
                service = AnalyticsService()

                _open.assert_called_with('keyfile.p12', ANY)
                SignedJwtAssertionCredentials.assert_called_with('a@example.com', ANY, scope=ANY)
                eq_(service.profile_id, 125)

    def test_get_data_http_error(self):
        """
        If an HttpError is rasied during _get_data, raise
        AnalyticsError.
        """
        query = self.service._service.data.return_value.ga.return_value.get.return_value

        # Mock HttpError because it requires some extra junk to
        # initialize that is annoying to provide.
        with patch('affiliates.links.google_analytics.HttpError', Exception) as HttpError:
            query.execute.side_effect = HttpError
            with self.assertRaises(AnalyticsError):
                self.service._get_data()

    def test_get_data(self):
        mock_get = self.service._service.data.return_value.ga.return_value.get
        eq_(self.service._get_data(foo='bar', baz=1), mock_get.return_value.execute.return_value)
        mock_get.assert_called_with(ids='ga:125', foo='bar', baz=1)

    def test_get_clicks_for_date_sampled_data(self):
        """
        If settings.DEBUG is false and the result has sampled data,
        raise AnalyticsError.
        """
        self.service._get_data = Mock(return_value={'containsSampledData': True})

        with self.assertRaises(AnalyticsError):
            self.service.get_clicks_for_date(date(2014, 1, 1))

    def test_get_clicks_for_date_sampled_data_default(self):
        """
        If the result doesn't say if it has sampled data or not, assume
        that it doesn't.
        """
        self.service._get_data = Mock(return_value={})
        eq_(self.service.get_clicks_for_date(date(2014, 1, 1)), {})

    def test_get_clicks_for_date_no_rows(self):
        """
        If no rows are returned from the API, return an empty dict.
        """
        self.service._get_data = Mock(return_value={'containsSampledData': False})
        eq_(self.service.get_clicks_for_date(date(2014, 1, 1)), {})

    def test_get_clicks_for_date(self):
        self.service._get_data = Mock(return_value={
            'containsSampledData': False,
            'rows': [['5', '4'], ['3', '2']]
        })
        eq_(self.service.get_clicks_for_date(date(2014, 1, 1)), {'5': '4', '3': '2'})
        self.service._get_data.assert_called_with(
            start_date='2014-01-01',
            end_date='2014-01-01',
            metrics='ga:pageviews',
            dimensions='ga:customVarValue1'
        )
