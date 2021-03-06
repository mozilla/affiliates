from datetime import timedelta

from django.db.models import F
from django.utils import timezone

from affiliates.base.management.commands import QuietCommand
from affiliates.links.models import DataPoint, Link


class Command(QuietCommand):
    help = ('Aggregate DataPoints older than 90 days.')

    def handle_quiet(self, *args, **kwargs):
        today = timezone.now().date()
        cutoff = today - timedelta(days=90)

        datapoints = DataPoint.objects.filter(date__lt=cutoff)
        total = datapoints.count()
        self.output('Aggregating old datapoints... (0/{0})'.format(total))
        for index, datapoint in enumerate(datapoints):
            if index % 1000 == 0:
                self.output('Aggregating old datapoints... ({0}/{1})'.format(index, total))

            Link.objects.filter(pk=datapoint.link.pk).update(
                aggregate_link_clicks=F('aggregate_link_clicks') + datapoint.link_clicks,
                aggregate_firefox_downloads=(F('aggregate_firefox_downloads') +
                                             datapoint.firefox_downloads),
            )

            # Bulk delete would be nicer, but this helps avoid stat
            # errors if we re-run after a failure.
            datapoint.delete()

        self.output('Done!')
