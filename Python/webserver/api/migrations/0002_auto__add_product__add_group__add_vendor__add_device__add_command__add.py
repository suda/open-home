# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table(u'core_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Vendor'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('role', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'api', ['Product'])

        # Adding model 'Group'
        db.create_table(u'core_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['Group'])

        # Adding model 'Vendor'
        db.create_table(u'core_vendor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['Vendor'])

        # Adding model 'Device'
        db.create_table(u'core_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Product'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Group'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('payload', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'api', ['Device'])

        # Adding model 'Command'
        db.create_table(u'core_command', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Device'])),
            ('sent_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('kind', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'api', ['Command'])

        # Adding model 'Update'
        db.create_table(u'core_update', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Device'])),
            ('received_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('kind', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('payload', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'api', ['Update'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'core_product')

        # Deleting model 'Group'
        db.delete_table(u'core_group')

        # Deleting model 'Vendor'
        db.delete_table(u'core_vendor')

        # Deleting model 'Device'
        db.delete_table(u'core_device')

        # Deleting model 'Command'
        db.delete_table(u'core_command')

        # Deleting model 'Update'
        db.delete_table(u'core_update')


    models = {
        u'api.command': {
            'Meta': {'object_name': 'Command'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.SmallIntegerField', [], {}),
            'sent_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'api.device': {
            'Meta': {'object_name': 'Device'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'payload': ('django.db.models.fields.TextField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Product']"}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'api.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.product': {
            'Meta': {'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'role': ('django.db.models.fields.SmallIntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Vendor']"})
        },
        u'api.update': {
            'Meta': {'object_name': 'Update'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.SmallIntegerField', [], {}),
            'payload': ('django.db.models.fields.TextField', [], {}),
            'received_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'api.vendor': {
            'Meta': {'object_name': 'Vendor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['api']