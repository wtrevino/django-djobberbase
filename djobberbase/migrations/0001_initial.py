# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('djobberbase_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('var_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
            ('title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_order', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, blank=True)),
        ))
        db.send_create_signal('djobberbase', ['Category'])

        # Adding model 'Type'
        db.create_table('djobberbase_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('var_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('djobberbase', ['Type'])

        # Adding model 'City'
        db.create_table('djobberbase_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('ascii_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('djobberbase', ['City'])

        # Adding model 'Job'
        db.create_table('djobberbase_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djobberbase.Category'])),
            ('jobtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djobberbase.Type'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_html', self.gf('django.db.models.fields.TextField')()),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('company_slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djobberbase.City'], null=True, blank=True)),
            ('outside_location', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=150, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 9, 0, 0))),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('views_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('auth', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('joburl', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('poster_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('apply_online', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('spotlight', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('djobberbase', ['Job'])

        # Adding model 'JobStat'
        db.create_table('djobberbase_jobstat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djobberbase.Job'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 9, 0, 0))),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('stat_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('djobberbase', ['JobStat'])

        # Adding model 'JobSearch'
        db.create_table('djobberbase_jobsearch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 9, 0, 0))),
        ))
        db.send_create_signal('djobberbase', ['JobSearch'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('djobberbase_category')

        # Deleting model 'Type'
        db.delete_table('djobberbase_type')

        # Deleting model 'City'
        db.delete_table('djobberbase_city')

        # Deleting model 'Job'
        db.delete_table('djobberbase_job')

        # Deleting model 'JobStat'
        db.delete_table('djobberbase_jobstat')

        # Deleting model 'JobSearch'
        db.delete_table('djobberbase_jobsearch')


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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.Category']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.City']", 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'company_slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 9, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.Type']"}),
            'joburl': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'outside_location': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'poster_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'spotlight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'}),
            'views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'djobberbase.jobsearch': {
            'Meta': {'object_name': 'JobSearch'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 9, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djobberbase.jobstat': {
            'Meta': {'object_name': 'JobStat'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 9, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djobberbase.Job']"}),
            'stat_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'djobberbase.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'var_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['djobberbase']