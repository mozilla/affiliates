# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'NewsItem'
        db.delete_table(u'news_newsitem')

        from django.contrib.contenttypes.models import ContentType
        ContentType.objects.filter(app_label='news').delete()



    def backwards(self, orm):
        # Adding model 'NewsItem'
        db.create_table(u'news_newsitem', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('news', ['NewsItem'])


    models = {

    }

    complete_apps = ['news']
