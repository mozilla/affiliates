from funfactory import admin

from stats.sites import StatsAdminMixin


# Monkeypatch admin site
# TODO: Do this for the built in admin instead.
old_admin_class = admin.site.__class__
admin.site.__class__ = type('StatsAdminSite',
                            (StatsAdminMixin, old_admin_class), {})
