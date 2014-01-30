# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'links_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('destination', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('html', self.gf('django.db.models.fields.TextField')()),
            ('aggregate_link_clicks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('aggregate_firefox_downloads', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('aggregate_firefox_os_referrals', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'links', ['Link'])

        # Adding model 'DataPoint'
        db.create_table(u'links_datapoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['links.Link'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('link_clicks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('firefox_downloads', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('firefox_os_referrals', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'links', ['DataPoint'])

        # Adding model 'LeaderboardStanding'
        db.create_table(u'links_leaderboardstanding', (
            ('ranking', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('metric', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'links', ['LeaderboardStanding'])


    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'links_link')

        # Deleting model 'DataPoint'
        db.delete_table(u'links_datapoint')

        # Deleting model 'LeaderboardStanding'
        db.delete_table(u'links_leaderboardstanding')


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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['links']