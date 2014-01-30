# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from south.v2 import DataMigration

from affiliates.shared.utils import absolutify, ugettext_locale


class Migration(DataMigration):
    depends_on = (
        ('badges', '0005_auto__del_field_clickstats_year__del_field_clickstats_month__del_uniqu'),
        ('banners', '0003_auto__add_imagebannervariation__add_textbanner__add_category__add_imag'),
    )

    def forwards(self, orm):
        for banner_instance in orm['banners.OldBannerInstance'].objects.all():
            try:
                badge_instance = orm['badges.BadgeInstance'].objects.get(pk=banner_instance.pk)

                html = '<a href="{url}"><img src="{src}" alt="{alt}" /></a>'.format(
                    url=absolutify('/link/banner/{pk}'.format(pk=banner_instance.pk), protocol=''),
                    src=absolutify(banner_instance.image.image.url, protocol=''),
                    alt=ugettext_locale(badge_instance.badge.name, banner_instance.image.locale)
                )

                new_link = orm['links.Link'](
                    user=badge_instance.user,
                    destination=badge_instance.badge.href,
                    html=html,
                    legacy_banner_instance_id=badge_instance.id,
                    legacy_banner_image_id=banner_instance.image.id
                )

                # Aggregate old stats.
                for stats in badge_instance.clickstats_set.all():
                    new_link.aggregate_link_clicks += stats.clicks

                new_link.save()
            except ObjectDoesNotExist:
                # Sometimes the data is bad and points to things that
                # don't exist. Only sane thing to do is THROW THE DATA
                # AWAY
                continue

    def backwards(self, orm):
        raise Exception('No take backs!')

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'badges.badge': {
            'Meta': {'object_name': 'Badge'},
            'child_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'href': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Subcategory']"})
        },
        u'badges.badgeinstance': {
            'Meta': {'object_name': 'BadgeInstance'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Badge']"}),
            'child_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'badges.badgepreview': {
            'Meta': {'unique_together': "(('locale', 'badge'),)", 'object_name': 'BadgePreview'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Badge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'locale': ('affiliates.shared.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        u'badges.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'badges.clickstats': {
            'Meta': {'unique_together': "(('badge_instance', 'datetime'),)", 'object_name': 'ClickStats'},
            'badge_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.BadgeInstance']"}),
            'clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'badges.leaderboard': {
            'Meta': {'object_name': 'Leaderboard'},
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ranking': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'badges.subcategory': {
            'Meta': {'object_name': 'Subcategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Category']"})
        },
        u'banners.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['banners.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'banners.imagebanner': {
            'Meta': {'object_name': 'ImageBanner'},
            'category': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['banners.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'banners.imagebannervariation': {
            'Meta': {'object_name': 'ImageBannerVariation'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['banners.ImageBanner']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'locale': ('affiliates.shared.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        u'banners.oldbanner': {
            'Meta': {'object_name': 'OldBanner', '_ormbases': [u'badges.Badge']},
            u'badge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['badges.Badge']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'banners.oldbannerimage': {
            'Meta': {'object_name': 'OldBannerImage'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['banners.OldBanner']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'locale': ('affiliates.shared.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        u'banners.oldbannerinstance': {
            'Meta': {'object_name': 'OldBannerInstance', '_ormbases': [u'badges.BadgeInstance']},
            u'badgeinstance_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['badges.BadgeInstance']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['banners.OldBannerImage']"})
        },
        u'banners.textbanner': {
            'Meta': {'object_name': 'TextBanner'},
            'category': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['banners.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'links.datapoint': {
            'Meta': {'object_name': 'DataPoint'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['links.Link']"}),
            'link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'links.leaderboardstanding': {
            'Meta': {'object_name': 'LeaderboardStanding'},
            'metric': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ranking': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'links.link': {
            'Meta': {'object_name': 'Link'},
            'aggregate_firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'aggregate_firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'aggregate_link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_banner_image_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'legacy_banner_instance_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['badges', 'banners', 'links']
    symmetrical = True
