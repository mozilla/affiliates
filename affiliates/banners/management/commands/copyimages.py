from django.core.management.base import BaseCommand

from affiliates.banners.models import BannerImage


class Command(BaseCommand):
    help = 'Copy images to the new filename format'

    def handle(self, *args, **options):
        for banner in BannerImage.objects.all():
            banner.image.save(banner.image.name, banner.image)
