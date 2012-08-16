from celery.decorators import task

from facebook.models import FacebookBannerInstance, FacebookClickStats
from facebook.utils import current_hour
from shared.utils import get_object_or_none


@task
def add_click(banner_instance_id):
    """Add a click to the specified banner instance."""
    banner_instance = get_object_or_none(FacebookBannerInstance,
                                         id=banner_instance_id)
    if banner_instance is not None:
        banner_instance.total_clicks += 1
        banner_instance.save()

        stats, created = (FacebookClickStats.objects
                          .get_or_create(hour=current_hour(),
                                         banner_instance=banner_instance))
        stats.clicks += 1
        stats.save()
