from collections import defaultdict

from django.db.models import Sum

from affiliates.banners.models import BANNER_TYPES, Category
from affiliates.base.management.commands import QuietCommand
from affiliates.links.models import Link


class Command(QuietCommand):
    help = ('Denormalize metrics like clicks and downloads.')

    METRICS = ('link_clicks', 'firefox_downloads', 'firefox_os_referrals')

    def handle_quiet(self, *args, **kwargs):
        # Running totals are stored in these dicts so that we don't have
        # to re-query the database to determine the totals for banners
        # and categories.
        category_totals = {}  # [metric][category_pk]
        banner_totals = {}  # [banner_class][metric][banner_pk]

        # Init dicts for storing running totals.
        for banner_type in BANNER_TYPES:
            banner_totals[banner_type] = {}
        for metric in self.METRICS:
            category_totals[metric] = defaultdict(int)
            for banner_type in BANNER_TYPES:
                banner_totals[banner_type][metric] = defaultdict(int)

        # Annotate links with the sum of the metrics from datapoints.
        links = Link.objects.prefetch_related('banner_variation__banner__category')
        for metric in self.METRICS:
            links = links.annotate(**{'datapoint_' + metric: Sum('datapoint__' + metric)})

        # Update totals on links.
        for link in links:
            if not link.banner:  # Orphaned links get ignored.
                continue

            for metric in self.METRICS:
                # Total is aggregate + datapoint sum.
                total = (getattr(link, 'aggregate_' + metric) +
                         (getattr(link, 'datapoint_' + metric) or 0))
                setattr(link, metric, total)

                category_totals[metric][link.banner.category.pk] += total
                banner_totals[link.banner.__class__][metric][link.banner.pk] += total

            link.save()

        # Update totals on banners.
        for banner_type, metrics in banner_totals.items():
            for banner in banner_type.objects.all():
                for metric, totals in metrics.items():
                    setattr(banner, metric, totals[banner.pk])
                banner.save()

        # Update totals on categories.
        for category in Category.objects.all():
            for metric, totals in category_totals.items():
                setattr(category, metric, totals[category.pk])
            category.save()

        self.output('Done!')
