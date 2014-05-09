from datetime import datetime, timedelta

from django.core.management.base import CommandError
from django.utils import timezone

from affiliates.base.management.commands import QuietCommand
from affiliates.base.utils import date_yesterday
from affiliates.links.google_analytics import AnalyticsError, AnalyticsService
from affiliates.links.models import DataPoint, Link


class Command(QuietCommand):
    help = ('Collect metrics from Google Analytics for the given day (format DD-MM-YYYY, defaults '
            'to two days ago if no date is given, uses UTC timezone).')
    args = '[date]'

    def handle_quiet(self, query_date=None, *args, **kwargs):
        try:
            service = AnalyticsService()
        except AnalyticsError as e:
            raise CommandError('Could not connect to analytics service: {0}'.format(e), e)

        if query_date:
            try:
                unaware_query_datetime = datetime.strptime(query_date, '%d-%m-%Y')
            except ValueError:
                raise CommandError('Date argument invalid. It must be in DD-MM-YYYY format')

            query_date = timezone.make_aware(unaware_query_datetime, timezone.utc).date()
        else:
            query_date = date_yesterday() - timedelta(days=1)

        self.output('Downloading click counts from GA...')
        try:
            clicks = service.get_clicks_for_date(query_date)
        except AnalyticsError as e:
            raise CommandError('Could not retrieve click data from analytics service: {0}'
                               .format(e))

        self.output('Adding datapoints to database...')
        datapoints = []
        for pk in Link.objects.values_list('id', flat=True):
            datapoint = DataPoint(link_id=pk, date=query_date,
                                  link_clicks=clicks.get(unicode(pk), 0))
            datapoints.append(datapoint)

        # Remove existing data, because supposedly our data is more
        # up-to-date.
        DataPoint.objects.filter(date=query_date).delete()
        DataPoint.objects.bulk_create(datapoints)

        self.output('Done!')
