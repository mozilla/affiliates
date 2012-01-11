# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('badges_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('badges', ['Category'])

        # Adding model 'Subcategory'
        db.create_table('badges_subcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('badges', ['Subcategory'])

        # Adding model 'Badge'
        db.create_table('badges_badge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('child_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Subcategory'])),
            ('href', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('badges', ['Badge'])

        # Adding model 'BadgeLocale'
        db.create_table('badges_badgelocale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locale', self.gf('shared.models.LocaleField')(default='en-US', max_length=32)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Badge'])),
        ))
        db.send_create_signal('badges', ['BadgeLocale'])

        # Adding model 'BadgePreview'
        db.create_table('badges_badgepreview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('locale', self.gf('shared.models.LocaleField')(default='en-US', max_length=32)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Badge'])),
        ))
        db.send_create_signal('badges', ['BadgePreview'])

        # Adding unique constraint on 'BadgePreview', fields ['locale', 'badge']
        db.create_unique('badges_badgepreview', ['locale', 'badge_id'])

        # Adding model 'BadgeInstance'
        db.create_table('badges_badgeinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('child_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Badge'])),
            ('clicks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('badges', ['BadgeInstance'])

        # Adding model 'ClickStats'
        db.create_table('badges_clickstats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.BadgeInstance'])),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('clicks', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('badges', ['ClickStats'])

        # Adding unique constraint on 'ClickStats', fields ['badge_instance', 'month', 'year']
        db.create_unique('badges_clickstats', ['badge_instance_id', 'month', 'year'])

        # Adding model 'Leaderboard'
        db.create_table('badges_leaderboard', (
            ('ranking', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('clicks', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('badges', ['Leaderboard'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ClickStats', fields ['badge_instance', 'month', 'year']
        db.delete_unique('badges_clickstats', ['badge_instance_id', 'month', 'year'])

        # Removing unique constraint on 'BadgePreview', fields ['locale', 'badge']
        db.delete_unique('badges_badgepreview', ['locale', 'badge_id'])

        # Deleting model 'Category'
        db.delete_table('badges_category')

        # Deleting model 'Subcategory'
        db.delete_table('badges_subcategory')

        # Deleting model 'Badge'
        db.delete_table('badges_badge')

        # Deleting model 'BadgeLocale'
        db.delete_table('badges_badgelocale')

        # Deleting model 'BadgePreview'
        db.delete_table('badges_badgepreview')

        # Deleting model 'BadgeInstance'
        db.delete_table('badges_badgeinstance')

        # Deleting model 'ClickStats'
        db.delete_table('badges_clickstats')

        # Deleting model 'Leaderboard'
        db.delete_table('badges_leaderboard')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'badges.badge': {
            'Meta': {'object_name': 'Badge'},
            'child_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'href': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.Subcategory']"})
        },
        'badges.badgeinstance': {
            'Meta': {'object_name': 'BadgeInstance'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.Badge']"}),
            'child_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'badges.badgelocale': {
            'Meta': {'object_name': 'BadgeLocale'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.Badge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('shared.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        'badges.badgepreview': {
            'Meta': {'unique_together': "(('locale', 'badge'),)", 'object_name': 'BadgePreview'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.Badge']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'locale': ('shared.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        'badges.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'badges.clickstats': {
            'Meta': {'unique_together': "(('badge_instance', 'month', 'year'),)", 'object_name': 'ClickStats'},
            'badge_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.BadgeInstance']"}),
            'clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'badges.leaderboard': {
            'Meta': {'object_name': 'Leaderboard'},
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ranking': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'badges.subcategory': {
            'Meta': {'object_name': 'Subcategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.Category']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['badges']
