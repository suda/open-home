# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.identifier'
        db.add_column(u'core_product', 'identifier',
                      self.gf('django.db.models.fields.CharField')(default=' ', max_length=32, db_index=True),
                      keep_default=False)

        # Adding field 'Vendor.identifier'
        db.add_column(u'core_vendor', 'identifier',
                      self.gf('django.db.models.fields.CharField')(default=' ', max_length=32, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.identifier'
        db.delete_column(u'core_product', 'identifier')

        # Deleting field 'Vendor.identifier'
        db.delete_column(u'core_vendor', 'identifier')


    models = {
        u'core.command': {
            'Meta': {'object_name': 'Command'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.SmallIntegerField', [], {}),
            'sent_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'core.device': {
            'Meta': {'object_name': 'Device'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'payload': ('django.db.models.fields.TextField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Product']"}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'core.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.product': {
            'Meta': {'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'role': ('django.db.models.fields.SmallIntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Vendor']"})
        },
        u'core.update': {
            'Meta': {'object_name': 'Update'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.SmallIntegerField', [], {}),
            'payload': ('django.db.models.fields.TextField', [], {}),
            'received_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.vendor': {
            'Meta': {'object_name': 'Vendor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']