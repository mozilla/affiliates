# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('banners', '0004_migrate_old_banners'),
        ('links', '0003_migrate_old_links'),
    )

    def forwards(self, orm):
        # Removing unique constraint on 'ClickStats', fields ['badge_instance', 'datetime']
        db.delete_unique(u'badges_clickstats', ['badge_instance_id', 'datetime'])

        # Removing unique constraint on 'BadgePreview', fields ['locale', 'badge']
        db.delete_unique(u'badges_badgepreview', ['locale', 'badge_id'])

        # Deleting model 'Category'
        db.delete_table(u'badges_category')

        # Deleting model 'Leaderboard'
        db.delete_table(u'badges_leaderboard')

        # Deleting model 'Badge'
        db.delete_table(u'badges_badge')

        # Deleting model 'BadgePreview'
        db.delete_table(u'badges_badgepreview')

        # Deleting model 'BadgeInstance'
        db.delete_table(u'badges_badgeinstance')

        # Deleting model 'ClickStats'
        db.delete_table(u'badges_clickstats')

        # Deleting model 'Subcategory'
        db.delete_table(u'badges_subcategory')

        from django.contrib.contenttypes.models import ContentType
        ContentType.objects.filter(app_label='badges').delete()


    def backwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'badges_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('badges', ['Category'])

        # Adding model 'Leaderboard'
        db.create_table(u'badges_leaderboard', (
            ('ranking', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('clicks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('badges', ['Leaderboard'])

        # Adding model 'Badge'
        db.create_table(u'badges_badge', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('child_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('displayed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('href', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Subcategory'])),
        ))
        db.send_create_signal('badges', ['Badge'])

        # Adding model 'BadgePreview'
        db.create_table(u'badges_badgepreview', (
            ('locale', self.gf('affiliates.shared.models.LocaleField')(default='en-US', max_length=32)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Badge'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('badges', ['BadgePreview'])

        # Adding unique constraint on 'BadgePreview', fields ['locale', 'badge']
        db.create_unique(u'badges_badgepreview', ['locale', 'badge_id'])

        # Adding model 'BadgeInstance'
        db.create_table(u'badges_badgeinstance', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('child_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('clicks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Badge'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('badges', ['BadgeInstance'])

        # Adding model 'ClickStats'
        db.create_table(u'badges_clickstats', (
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.BadgeInstance'])),
            ('clicks', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('badges', ['ClickStats'])

        # Adding unique constraint on 'ClickStats', fields ['badge_instance', 'datetime']
        db.create_unique(u'badges_clickstats', ['badge_instance_id', 'datetime'])

        # Adding model 'Subcategory'
        db.create_table(u'badges_subcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('badges', ['Subcategory'])


    models = {

    }

    complete_apps = ['badges']
