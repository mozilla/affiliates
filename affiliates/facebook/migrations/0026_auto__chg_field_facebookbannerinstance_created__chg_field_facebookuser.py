# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FacebookBannerInstance.created'
        db.alter_column(u'facebook_facebookbannerinstance', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'FacebookUser.created'
        db.alter_column(u'facebook_facebookuser', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'FacebookBannerInstance.created'
        db.alter_column(u'facebook_facebookbannerinstance', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'FacebookUser.created'
        db.alter_column(u'facebook_facebookuser', 'created', self.gf('django.db.models.fields.DateTimeField')())

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'facebook.appnotification': {
            'Meta': {'object_name': 'AppNotification'},
            'format_argument': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['facebook.FacebookUser']"})
        },
        u'facebook.facebookaccountlink': {
            'Meta': {'object_name': 'FacebookAccountLink'},
            'activation_code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'affiliates_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account_links'", 'to': u"orm['auth.User']"}),
            'facebook_user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'_account_link'", 'unique': 'True', 'to': u"orm['facebook.FacebookUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'facebook.facebookbanner': {
            'Meta': {'object_name': 'FacebookBanner'},
            '_alt_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'link': ('django.db.models.fields.URLField', [], {'default': "'https://www.mozilla.org/firefox'", 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Banner'", 'unique': 'True', 'max_length': '255'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'})
        },
        u'facebook.facebookbannerinstance': {
            'Meta': {'object_name': 'FacebookBannerInstance'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['facebook.FacebookBanner']"}),
            'can_be_an_ad': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'custom_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('affiliates.base.models.LocaleField', [], {'default': "'en-us'", 'max_length': '32'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'review_status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'total_clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'banner_instance_set'", 'to': u"orm['facebook.FacebookUser']"})
        },
        u'facebook.facebookbannerlocale': {
            'Meta': {'object_name': 'FacebookBannerLocale'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locale_set'", 'to': u"orm['facebook.FacebookBanner']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'locale': ('affiliates.base.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        },
        u'facebook.facebookclickstats': {
            'Meta': {'object_name': 'FacebookClickStats'},
            'banner_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['facebook.FacebookBannerInstance']"}),
            'clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hour': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 26, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'facebook.facebookuser': {
            'Meta': {'object_name': 'FacebookUser'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'leaderboard_position': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'total_clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['facebook']