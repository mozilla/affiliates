from django.db.models import F

from celery.decorators import task

from affiliates.links.models import Link


@task
def add_click(link_id, date_today):
    """Increment the click count for a link."""
    try:
        link = Link.objects.get(id=link_id)
    except Link.DoesNotExist:
        return

    datapoint, created = link.datapoint_set.get_or_create(date=date_today)
    datapoint.link_clicks = F('link_clicks') + 1
    datapoint.save()
