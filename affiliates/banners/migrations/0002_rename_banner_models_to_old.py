# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
         # Renaming models to old.
        db.rename_table('banners_banner', 'banners_oldbanner')
        db.rename_table('banners_bannerinstance', 'banners_oldbannerinstance')
        db.rename_table('banners_bannerimage', 'banners_oldbannerimage')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='banners', model='banner').update(model='oldbanner')
            orm['contenttypes.contenttype'].objects.filter(
                app_label='banners', model='bannerinstance').update(model='oldbannerinstance')
            orm['contenttypes.contenttype'].objects.filter(
                app_label='banners', model='bannerimage').update(model='oldbannerimage')

    def backwards(self, orm):
        # Renaming models back from old.
        db.rename_table('banners_oldbanner', 'banners_banner')
        db.rename_table('banners_oldbannerinstance', 'banners_bannerinstance')
        db.rename_table('banners_oldbannerimage', 'banners_bannerimage')
        if not db.dry_run:
            orm['contenttypes.contenttype'].objects.filter(
                app_label='banners', model='oldbanner').update(model='banner')
            orm['contenttypes.contenttype'].objects.filter(
                app_label='banners', model='oldbannerinstance').update(model='bannerinstance')
            orm['contenttypes.contenttype'].objects.filter(
                app_label='banners', model='oldbannerimage').update(model='bannerimage')



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
        u'badges.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'badges.subcategory': {
            'Meta': {'object_name': 'Subcategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Category']"})
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['banners']
