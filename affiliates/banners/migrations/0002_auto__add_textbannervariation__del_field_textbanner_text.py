# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TextBannerVariation'
        db.create_table(u'banners_textbannervariation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('banner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variation_set', to=orm['banners.TextBanner'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('locale', self.gf('affiliates.base.models.LocaleField')(default='en-US', max_length=32)),
        ))
        db.send_create_signal(u'banners', ['TextBannerVariation'])

        # Deleting field 'TextBanner.text'
        db.delete_column(u'banners_textbanner', 'text')


    def backwards(self, orm):
        # Deleting model 'TextBannerVariation'
        db.delete_table(u'banners_textbannervariation')

        # Adding field 'TextBanner.text'
        db.add_column(u'banners_textbanner', 'text',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


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
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variation_set'", 'to': u"orm['banners.ImageBanner']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'locale': ('affiliates.base.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'})
        },
        u'banners.textbanner': {
            'Meta': {'object_name': 'TextBanner'},
            'category': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['banners.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'banners.textbannervariation': {
            'Meta': {'object_name': 'TextBannerVariation'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variation_set'", 'to': u"orm['banners.TextBanner']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('affiliates.base.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['banners']