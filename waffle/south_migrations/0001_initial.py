# encoding: utf-8
import datetime
import django

from south.db import db
from south.v2 import SchemaMigration
from django.db import models


# Django 1.5+ compatibility
if django.VERSION >= (1, 5):
    from django.contrib.auth import get_user_model
else:
    from django.contrib.auth.models import User

    def get_user_model():
        return User

User = get_user_model()
user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Flag'
        db.create_table('waffle_flag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('everyone', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=1, blank=True)),
            ('superusers', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('authenticated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rollout', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('waffle', ['Flag'])

        # Adding M2M table for field groups on 'Flag'
        db.create_table('waffle_flag_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('flag', models.ForeignKey(orm['waffle.flag'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('waffle_flag_groups', ['flag_id', 'group_id'])

        # Adding M2M table for field users on 'Flag'
        db.create_table('waffle_flag_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('flag', models.ForeignKey(orm['waffle.flag'], null=False)),
            (User._meta.model_name, models.ForeignKey(orm[user_orm_label], null=False))
        ))
        db.create_unique('waffle_flag_users', ['flag_id', ('%s_id') % User._meta.model_name])

        # Adding model 'Switch'
        db.create_table('waffle_switch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('waffle', ['Switch'])


    def backwards(self, orm):
        
        # Deleting model 'Flag'
        db.delete_table('waffle_flag')

        # Removing M2M table for field groups on 'Flag'
        db.delete_table('waffle_flag_groups')

        # Removing M2M table for field users on 'Flag'
        db.delete_table('waffle_flag_users')

        # Deleting model 'Switch'
        db.delete_table('waffle_switch')


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
	user_model_label: {
            'Meta': {
                'object_name': User.__name__,
                'db_table': "'%s'" % User._meta.db_table
            },
            User._meta.pk.attname: (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True',
                'db_column': "'%s'" % User._meta.pk.column}
            ),
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'waffle.flag': {
            'Meta': {'object_name': 'Flag'},
            'authenticated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'everyone': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '1', 'blank': 'True'}),
            'rollout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'superusers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm[user_orm_label]", 'symmetrical': 'False', 'blank': 'True'})
        },
        'waffle.switch': {
            'Meta': {'object_name': 'Switch'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['waffle']
