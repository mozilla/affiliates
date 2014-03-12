from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.utils import timezone

from affiliates.links.google_analytics import AnalyticsError, AnalyticsService
from affiliates.links.models import DataPoint, Link


class Command(BaseCommand):
    help = ('Collect metrics from Google Analytics for the previous day.')

    def handle(self, *args, **kwargs):
        try:
            service = AnalyticsService()
        except AnalyticsError as e:
            raise CommandError('Could not connect to analytics service: {0}'.format(e), e)

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        print 'Downloading click counts from GA...'
        try:
            clicks = service.get_clicks_for_date(yesterday)
        except AnalyticsError as e:
            raise CommandError('Could not retrieve click data from analytics service: {0}'
                               .format(e))

        print 'Adding datapoints to database...'
        datapoints = []
        for pk in Link.objects.values_list('id', flat=True):
            datapoint = DataPoint(link_id=pk, date=yesterday,
                                  link_clicks=clicks.get(unicode(pk), 0))
            datapoints.append(datapoint)

        try:
            DataPoint.objects.bulk_create(datapoints)
        except IntegrityError as e:
            raise CommandError('Could not insert datapoints into database due to IntegrityError.', e)

        print 'Done!'
