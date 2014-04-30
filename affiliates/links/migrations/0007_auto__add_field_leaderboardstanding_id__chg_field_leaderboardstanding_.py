# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing primary key index on 'LeaderboardStanding', fields ['ranking']
        db.delete_primary_key(u'links_leaderboardstanding')

        # Adding field 'LeaderboardStanding.id'
        db.add_column(u'links_leaderboardstanding', u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))


        # Changing field 'LeaderboardStanding.ranking'
        db.alter_column(u'links_leaderboardstanding', 'ranking', self.gf('django.db.models.fields.PositiveIntegerField')())
        # Adding unique constraint on 'LeaderboardStanding', fields ['ranking', 'metric']
        db.create_unique(u'links_leaderboardstanding', ['ranking', 'metric'])


    def backwards(self, orm):
        # Removing unique constraint on 'LeaderboardStanding', fields ['ranking', 'metric']
        db.delete_unique(u'links_leaderboardstanding', ['ranking', 'metric'])

        # Deleting field 'LeaderboardStanding.id'
        db.delete_column(u'links_leaderboardstanding', u'id')


        # Changing field 'LeaderboardStanding.ranking'
        db.alter_column(u'links_leaderboardstanding', 'ranking', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True))
        # Adding primary key index on 'LeaderboardStanding', fiels['ranking']
        db.create_primary_key(u'links_leaderboardstanding', [u'ranking'])


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
        u'links.datapoint': {
            'Meta': {'unique_together': "(('link', 'date'),)", 'object_name': 'DataPoint'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['links.Link']"}),
            'link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'links.leaderboardstanding': {
            'Meta': {'unique_together': "(('ranking', 'metric'),)", 'object_name': 'LeaderboardStanding'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ranking': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'links.link': {
            'Meta': {'object_name': 'Link'},
            'aggregate_firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'aggregate_firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'aggregate_link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'banner_type': ('django.db.models.fields.CharField', [], {'default': "'image_banner'", 'max_length': '255'}),
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

    complete_apps = ['links']
