from datetime import datetime

from celery.decorators import task

from banners.models import BannerInstance

@task
def add_click(banner_instance_id):
    """Increment the click count for a banner instance."""
    now = datetime.now()
    try:
        instance = BannerInstance.objects.get(pk=banner_instance_id)
    except BannerInstance.DoesNotExist:
        return

    instance.add_click(now.year, now.month)


@task
def old_add_click(user_id, banner_id, banner_img_id):
    """Increment the click counter for an existing banner instance."""
    now = datetime.now()

    try:
        instance = BannerInstance.objects.get(user=user_id,
                                              badge=banner_id,
                                              image=banner_img_id)
    except BannerInstance.DoesNotExist:
        # Because this type of link is deprecated, we do not create new
        # banner instances with it.
        return

    instance.add_click(now.year, now.month)
