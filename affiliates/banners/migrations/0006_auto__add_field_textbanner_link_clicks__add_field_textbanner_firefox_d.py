# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TextBanner.link_clicks'
        db.add_column(u'banners_textbanner', 'link_clicks',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'TextBanner.firefox_downloads'
        db.add_column(u'banners_textbanner', 'firefox_downloads',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'TextBanner.firefox_os_referrals'
        db.add_column(u'banners_textbanner', 'firefox_os_referrals',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Category.link_clicks'
        db.add_column(u'banners_category', 'link_clicks',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Category.firefox_downloads'
        db.add_column(u'banners_category', 'firefox_downloads',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Category.firefox_os_referrals'
        db.add_column(u'banners_category', 'firefox_os_referrals',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ImageBanner.link_clicks'
        db.add_column(u'banners_imagebanner', 'link_clicks',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ImageBanner.firefox_downloads'
        db.add_column(u'banners_imagebanner', 'firefox_downloads',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ImageBanner.firefox_os_referrals'
        db.add_column(u'banners_imagebanner', 'firefox_os_referrals',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'FirefoxUpgradeBanner.link_clicks'
        db.add_column(u'banners_firefoxupgradebanner', 'link_clicks',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'FirefoxUpgradeBanner.firefox_downloads'
        db.add_column(u'banners_firefoxupgradebanner', 'firefox_downloads',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'FirefoxUpgradeBanner.firefox_os_referrals'
        db.add_column(u'banners_firefoxupgradebanner', 'firefox_os_referrals',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TextBanner.link_clicks'
        db.delete_column(u'banners_textbanner', 'link_clicks')

        # Deleting field 'TextBanner.firefox_downloads'
        db.delete_column(u'banners_textbanner', 'firefox_downloads')

        # Deleting field 'TextBanner.firefox_os_referrals'
        db.delete_column(u'banners_textbanner', 'firefox_os_referrals')

        # Deleting field 'Category.link_clicks'
        db.delete_column(u'banners_category', 'link_clicks')

        # Deleting field 'Category.firefox_downloads'
        db.delete_column(u'banners_category', 'firefox_downloads')

        # Deleting field 'Category.firefox_os_referrals'
        db.delete_column(u'banners_category', 'firefox_os_referrals')

        # Deleting field 'ImageBanner.link_clicks'
        db.delete_column(u'banners_imagebanner', 'link_clicks')

        # Deleting field 'ImageBanner.firefox_downloads'
        db.delete_column(u'banners_imagebanner', 'firefox_downloads')

        # Deleting field 'ImageBanner.firefox_os_referrals'
        db.delete_column(u'banners_imagebanner', 'firefox_os_referrals')

        # Deleting field 'FirefoxUpgradeBanner.link_clicks'
        db.delete_column(u'banners_firefoxupgradebanner', 'link_clicks')

        # Deleting field 'FirefoxUpgradeBanner.firefox_downloads'
        db.delete_column(u'banners_firefoxupgradebanner', 'firefox_downloads')

        # Deleting field 'FirefoxUpgradeBanner.firefox_os_referrals'
        db.delete_column(u'banners_firefoxupgradebanner', 'firefox_os_referrals')


    models = {
        u'banners.category': {
            'Meta': {'object_name': 'Category'},
            'firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'firefox_downloads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'firefox_os_referrals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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