"""Add all existing locales as enabled for all badges."""
from badges.models import Badge, BadgeLocale, LANGUAGE_CHOICES


def run():
    locales = [lang[0] for lang in LANGUAGE_CHOICES]

    for badge in Badge.objects.all():
        badge_locales = [BadgeLocale(badge=badge, locale=locale)
                         for locale in locales]
        badge.badgelocale_set.all().delete()
        badge.badgelocale_set = badge_locales
        badge.save()
