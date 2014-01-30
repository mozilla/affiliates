# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        from django.contrib.contenttypes.models import ContentType

        # Deleting model 'OldBanner'
        db.delete_table(u'banners_oldbanner')
        ContentType.objects.filter(app_label='banners', model='oldbanner').delete()

        # Deleting model 'OldBannerImage'
        db.delete_table(u'banners_oldbannerimage')
        ContentType.objects.filter(app_label='banners', model='oldbannerimage').delete()

        # Deleting model 'OldBannerInstance'
        db.delete_table(u'banners_oldbannerinstance')
        ContentType.objects.filter(app_label='banners', model='oldbannerinstance').delete()


    def backwards(self, orm):
        # Adding model 'OldBanner'
        db.create_table(u'banners_oldbanner', (
            (u'badge_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['badges.Badge'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'banners', ['OldBanner'])

        # Adding model 'OldBannerImage'
        db.create_table(u'banners_oldbannerimage', (
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('locale', self.gf('affiliates.shared.models.LocaleField')(default='en-US', max_length=32)),
            ('banner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banners.OldBanner'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'banners', ['OldBannerImage'])

        # Adding model 'OldBannerInstance'
        db.create_table(u'banners_oldbannerinstance', (
            (u'badgeinstance_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['badges.BadgeInstance'], unique=True, primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['banners.OldBannerImage'])),
        ))
        db.send_create_signal(u'banners', ['OldBannerInstance'])


    models = {
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
        }
    }

    complete_apps = ['banners']
