# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Sample', fields ['name']
        db.delete_unique(u'waffle_sample', ['name'])

        # Removing unique constraint on 'Switch', fields ['name']
        db.delete_unique(u'waffle_switch', ['name'])

        # Removing unique constraint on 'Flag', fields ['name']
        db.delete_unique(u'waffle_flag', ['name'])

        # Adding field 'Flag.site'
        db.add_column(u'waffle_flag', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='waffle_flags', null=True, to=orm['sites.Site']),
                      keep_default=False)

        # Adding unique constraint on 'Flag', fields ['name', 'site']
        db.create_unique(u'waffle_flag', ['name', 'site_id'])

        # Adding field 'Switch.site'
        db.add_column(u'waffle_switch', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='waffle_switches', null=True, to=orm['sites.Site']),
                      keep_default=False)

        # Adding unique constraint on 'Switch', fields ['name', 'site']
        db.create_unique(u'waffle_switch', ['name', 'site_id'])

        # Adding field 'Sample.site'
        db.add_column(u'waffle_sample', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='waffle_samples', null=True, to=orm['sites.Site']),
                      keep_default=False)

        # Adding unique constraint on 'Sample', fields ['name', 'site']
        db.create_unique(u'waffle_sample', ['name', 'site_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Sample', fields ['name', 'site']
        db.delete_unique(u'waffle_sample', ['name', 'site_id'])

        # Removing unique constraint on 'Switch', fields ['name', 'site']
        db.delete_unique(u'waffle_switch', ['name', 'site_id'])

        # Removing unique constraint on 'Flag', fields ['name', 'site']
        db.delete_unique(u'waffle_flag', ['name', 'site_id'])

        # Deleting field 'Flag.site'
        db.delete_column(u'waffle_flag', 'site_id')

        # Adding unique constraint on 'Flag', fields ['name']
        db.create_unique(u'waffle_flag', ['name'])

        # Deleting field 'Switch.site'
        db.delete_column(u'waffle_switch', 'site_id')

        # Adding unique constraint on 'Switch', fields ['name']
        db.create_unique(u'waffle_switch', ['name'])

        # Deleting field 'Sample.site'
        db.delete_column(u'waffle_sample', 'site_id')

        # Adding unique constraint on 'Sample', fields ['name']
        db.create_unique(u'waffle_sample', ['name'])


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.portaluser': {
            'Meta': {'object_name': 'PortalUser'},
            'activation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'waffle.flag': {
            'Meta': {'unique_together': "(('name', 'site'),)", 'object_name': 'Flag'},
            'authenticated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'everyone': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '1', 'blank': 'True'}),
            'rollout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'waffle_flags'", 'null': 'True', 'to': u"orm['sites.Site']"}),
            'staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'superusers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'testing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.PortalUser']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'waffle.sample': {
            'Meta': {'unique_together': "(('name', 'site'),)", 'object_name': 'Sample'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'waffle_samples'", 'null': 'True', 'to': u"orm['sites.Site']"})
        },
        u'waffle.switch': {
            'Meta': {'unique_together': "(('name', 'site'),)", 'object_name': 'Switch'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'waffle_switches'", 'null': 'True', 'to': u"orm['sites.Site']"})
        }
    }

    complete_apps = ['waffle']