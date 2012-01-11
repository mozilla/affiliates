# encoding: utf8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding constraint on auth.User's email fields
        db.create_unique('auth_user', ['email'])

    def backwards(self, orm):
        db.delete_index('auth_user', ['email'])

    models = {}
    complete_apps = ['django.contrib.auth']
