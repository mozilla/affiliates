# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Banner'
        db.create_table('banners_banner', (
            ('badge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['badges.Badge'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('banners', ['Banner'])

        # Adding model 'BannerImage'
        db.create_table('banners_bannerimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('banner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banners.Banner'])),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('locale', self.gf('shared.models.LocaleField')(default='en-US', max_length=32)),
        ))
        db.send_create_signal('banners', ['BannerImage'])

        # Adding model 'BannerInstance'
        db.create_table('banners_bannerinstance', (
            ('badgeinstance_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['badges.BadgeInstance'], unique=True, primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banners.BannerImage'])),
        ))
        db.send_create_signal('banners', ['BannerInstance'])


    def backwards(self, orm):
        
        # Deleting model 'Banner'
        db.delete_table('banners_banner')

        # Deleting model 'BannerImage'
        db.delete_table('banners_bannerimage')

        # Deleting model 'BannerInstance'
        db.delete_table('banners_bannerinstance')


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
        'badges.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'badges.subcategory': {
            'Meta': {'object_name': 'Subcategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['badges.Category']"})
        },
        'banners.banner': {
            'Meta': {'object_name': 'Banner', '_ormbases': ['badges.Badge']},
            'badge_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['badges.Badge']", 'unique': 'True', 'primary_key': 'True'})
        },
        'banners.bannerimage': {
            'Meta': {'object_name': 'BannerImage'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['banners.Banner']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'locale': ('shared.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        'banners.bannerinstance': {
            'Meta': {'object_name': 'BannerInstance', '_ormbases': ['badges.BadgeInstance']},
            'badgeinstance_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['badges.BadgeInstance']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['banners.BannerImage']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['banners']
