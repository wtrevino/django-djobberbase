# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field sites on 'Job'
        db.create_table('djobberbase_job_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['djobberbase.job'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('djobberbase_job_sites', ['job_id', 'site_id'])


    def backwards(self, orm):
        # Removing M2M table for field sites on 'Job'
        db.delete_table('djobberbase_job_sites')


    models = {
        'djobberbase.category': {
            'Meta': {'object_name': 'Category'},
            'category_order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'var_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        'djobberbase.city': {
            'Meta': {'object_name': 'City'},
            'ascii_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'djobberbase.job': {
            'Meta': {'object_name': 'Job'},
            'apply_online': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auth': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.Category']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.City']", 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'company_slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 10, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.Type']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'joburl': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'outside_location': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'poster_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'spotlight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'}),
            'views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'djobberbase.jobsearch': {
            'Meta': {'object_name': 'JobSearch'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 10, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djobberbase.jobstat': {
            'Meta': {'object_name': 'JobStat'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 10, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.Job']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'stat_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'djobberbase.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'var_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['djobberbase']