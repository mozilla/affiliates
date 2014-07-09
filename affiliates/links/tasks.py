from django.db.models import F

from celery.decorators import task

from affiliates.links.models import Link


@task
def add_click(link_id, date_today):
    """Increment the click count for a link."""
    try:
        link = Link.objects.prefetch_related('banner_variation__banner__category').get(id=link_id)
    except Link.DoesNotExist:
        return

    datapoint, created = link.datapoint_set.get_or_create(date=date_today)
    datapoint.link_clicks = F('link_clicks') + 1
    datapoint.save()

    # Update denormalized counts.
    link.link_clicks = F('link_clicks') + 1
    link.save()

    banner = link.banner
    banner.link_clicks = F('link_clicks') + 1
    banner.save()

    category = banner.category
    category.link_clicks = F('link_clicks') + 1
    category.save()
