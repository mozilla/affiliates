from StringIO import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

import commonware
import requests
from celery.decorators import task
from PIL import Image

from facebook.models import FacebookBannerInstance, FacebookClickStats
from facebook.utils import current_hour
from shared.utils import get_object_or_none


log = commonware.log.getLogger('a.facebook')


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


@task
def generate_banner_instance_image(banner_instance_id):
    """
    Create an image for a banner image by adding the user's profile image to the
    banner image.
    """
    banner_instance = get_object_or_none(FacebookBannerInstance,
                                         id=banner_instance_id)
    if banner_instance is not None:
        banner_image_file = banner_instance.banner.image

        # Grab the user's photo from Facebook
        try:
            r = requests.get('https://graph.facebook.com/%s/picture' %
                             banner_instance.user.id)
        except requests.exceptions.RequestException:
            # Log and retry later.
            log.error('Error downloading photo for user: %s' %
                      banner_instance.user.id)
            generate_banner_instance_image.delay(banner_instance_id)
            return

        user_image = Image.open(StringIO(r.content))
        banner_image = Image.open(banner_image_file)

        # Resize user image to expected size.
        user_image = user_image.resize(settings.FACEBOOK_CUSTOM_IMG_SIZE,
                                       Image.ANTIALIAS)

        # Generate the actual image.
        custom_image = banner_image.copy()
        custom_image.paste(user_image, settings.FACEBOOK_CUSTOM_IMG_COORDS)

        # Store the image in memory so we can save it to the model.
        io = StringIO()
        custom_image.save(io, format='JPEG')
        custom_image_file = InMemoryUploadedFile(io, None, 'custom_image.jpg',
                                                 'image/jpeg', io.len, None)
        banner_instance.custom_image.save('custom_image.jpg', custom_image_file)
