from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import connection

from multidb.pinning import use_master

from affiliates.banners.models import Category, ImageBanner, ImageBannerVariation
from affiliates.base.utils import absolutify
from affiliates.links.models import Link


class Command(BaseCommand):
    help = ('Migrate link data from an Affiliates v1 database.')
    args = ('[old_table_prefix]')

    @use_master
    def handle(self, old_table_prefix, *args, **kwargs):
        cursor = connection.cursor()

        # Categories
        # Cannot use bulk_create due to django-mptt.
        cursor.execute('SELECT id, name FROM {0}badges_category'.format(old_table_prefix))
        for row in cursor.fetchall():
            Category.objects.create(id=row[0], name=row[1])

        subcategory_to_category = {}
        cursor.execute('SELECT id, name, parent_id FROM {0}badges_subcategory'
                       .format(old_table_prefix))
        for row in cursor.fetchall():
            category = Category.objects.create(name=row[1], parent_id=row[2])
            subcategory_to_category[row[0]] = category.id

        # Banners
        cursor.execute('SELECT subcategory_id, name, href, displayed, id FROM {0}badges_badge'
                       .format(old_table_prefix))
        banners = [
            ImageBanner(
                id=row[4],
                category_id=subcategory_to_category[row[0]],
                name=row[1],
                destination=row[2],
                visible=row[3]
            ) for row in cursor.fetchall()
        ]
        ImageBanner.objects.bulk_create(banners, batch_size=1000)

        # Banner Images
        cursor.execute('SELECT id, banner_id, color, locale, image FROM {0}banners_bannerimage'
                       .format(old_table_prefix))
        variations = [
            ImageBannerVariation(
                id=row[0],
                banner_id=row[1],
                color=row[2],
                locale=row[3],
                image=row[4],
            ) for row in cursor.fetchall()
        ]
        ImageBannerVariation.objects.bulk_create(variations, batch_size=1000)

        # Links! (this is the big one)
        content_type = ContentType.objects.get_for_model(ImageBannerVariation)
        cursor.execute("""SELECT
            badgeinstance.id, badgeinstance.user_id, badgeinstance.badge_id, badgeinstance.clicks,
            bannerinstance.image_id, badge.href, bannerimage.image, bannerimage.id
        FROM {0}badges_badgeinstance AS badgeinstance
        LEFT JOIN {0}banners_bannerinstance AS bannerinstance ON
            bannerinstance.badgeinstance_ptr_id = badgeinstance.id
        LEFT JOIN {0}badges_badge AS badge ON badgeinstance.badge_id = badge.id
        LEFT JOIN {0}banners_bannerimage AS bannerimage ON bannerinstance.image_id = bannerimage.id
        """.format(old_table_prefix))
        links = [
            Link(
                id=row[0],
                user_id=row[1],
                destination=row[5],
                html=u'<a href="{url}"><img src="{src}" alt="" /></a>'.format(
                    url=absolutify(u'/link/banner/{0}'.format(row[0]), protocol=''),
                    src=absolutify(u'/media/{0}'.format(row[6]), protocol='')
                ),
                legacy_banner_instance_id=row[0],
                legacy_banner_image_id=row[4],
                aggregate_link_clicks=row[3],
                banner_variation_id=row[7],
                banner_variation_content_type=content_type
            ) for row in cursor.fetchall()
        ]
        Link.objects.bulk_create(links, batch_size=1000)
