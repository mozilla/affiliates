# -*- coding: utf-8 -*-
from south.v2 import DataMigration

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Re-save variations to update their dimensions.
        for variation in orm['banners.ImageBannerVariation'].objects.all():
            variation.width = variation.image.width
            variation.height = variation.image.height
            variation.save()

        for variation in orm['banners.FirefoxUpgradeBannerVariation'].objects.all():
            variation.width = variation.image.width
            variation.height = variation.image.height
            variation.save()

    def backwards(self, orm):
        "Write your backwards methods here."

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
        u'banners.firefoxupgradebanner': {
            'Meta': {'object_name': 'FirefoxUpgradeBanner'},
            'category': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['banners.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'banners.firefoxupgradebannervariation': {
            'Meta': {'object_name': 'FirefoxUpgradeBannerVariation'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variation_set'", 'to': u"orm['banners.FirefoxUpgradeBanner']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'locale': ('affiliates.base.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'}),
            'upgrade_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'locale': ('affiliates.base.models.LocaleField', [], {'default': "'en-US'", 'max_length': '32'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
    symmetrical = True
