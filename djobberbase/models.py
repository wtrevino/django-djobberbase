# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str, force_unicode
from django.utils.translation import ugettext_lazy as _
from djobberbase.helpers import last_hour, getIP
from djobberbase.managers import ActiveJobsManager, TempJobsManager
from djobberbase.conf import settings as djobberbase_settings
import datetime
import uuid
import time
try: 
   from hashlib import md5
except ImportError:
   from md5 import md5

class Category(models.Model):
    ''' The Category model, very straight forward. Includes a get_total_jobs
        method that returns the total of jobs with that category.
        The save() method is overriden so it can automatically asign
        a category order in case no one is provided.
    '''
    name = models.CharField(_('Name'), unique=True, max_length=32, blank=False)
    var_name = models.SlugField(_('Slug'), unique=True, max_length=32, blank=False)
    title = models.TextField(_('Title'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    keywords = models.TextField(_('Keywords'), blank=True)
    category_order = models.PositiveIntegerField(_('Category order'), 
                                                    unique=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_total_jobs(self):
        return Job.active.filter(category=self).count()

    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('djobberbase_job_list_category', [self.var_name])

    def save(self, *args, **kwargs):
        if not self.category_order:
            try:
                self.category_order = Category.objects.\
                                    latest('category_order').category_order + 1
            except Category.DoesNotExist:
                self.category_order = 0
        if not self.var_name:
            self.var_name = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Type(models.Model):
    ''' The Type model, nothing special, just the name and
        var_name fields. Again, the var_name is slugified by the overriden
        save() method in case it's not provided.
    '''
    name = models.CharField(_('Name'), unique=True, max_length=16, blank=False)
    var_name = models.SlugField(_('Slug'), unique=True, max_length=32, blank=False)

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.var_name:
            self.var_name = slugify(self.name)
        super(Type, self).save(*args, **kwargs)        

class City(models.Model):
    ''' A model for cities, with a get_total_jobs method to get
        the total of jobs in that city, save() method is overriden
        to slugify name to ascii_name.
    '''
    name = models.CharField(_('Name'), unique=True, max_length=50, blank=False)
    ascii_name = models.SlugField(_('ASCII Name'), unique=True, max_length=50, blank=False)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def get_total_jobs(self):
        return Job.active.filter(city=self).count()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.ascii_name:
            self.ascii_name = slugify(self.name)
        super(City, self).save(*args, **kwargs) 

class Job(models.Model):
    ''' The basic job model.
    '''
    INACTIVE = 0
    TEMPORARY = 1
    ACTIVE = 2
    JOB_STATUS_CHOICES = (
        (INACTIVE, _('Inactive')),
        (TEMPORARY, _('Temporary')),
        (ACTIVE, _('Active'))
    )
    category = models.ForeignKey(Category, verbose_name=_('Category'), blank=False, null=False)
    jobtype = models.ForeignKey(Type, verbose_name=_('Job Type'), blank=False, null=False)
    title = models.CharField(verbose_name=_('Title'), max_length=100, blank=False)
    description = models.TextField(_('Description'), blank=False)
    description_html = models.TextField(editable=False)
    company = models.CharField(_('Company'), max_length=150, blank=False)
    company_slug = models.SlugField(max_length=150, 
                                            blank=False, editable=False)
    city = models.ForeignKey(City, verbose_name=_('City'), null=True, blank=True)
    outside_location = models.CharField(_('Outside location'), max_length=150, blank=True)
    #url of the company
    url = models.URLField(verify_exists=False, max_length=150, blank=True)    
    created_on = models.DateTimeField(_('Created on'), editable=False, \
                                        default=datetime.datetime.now())
    status = models.IntegerField(choices=JOB_STATUS_CHOICES, default=TEMPORARY)
    views_count = models.IntegerField(editable=False, default=0)
    auth = models.CharField(blank=True, editable=False, max_length=32)
    #url of the job post
    joburl = models.CharField(blank=True, editable=False, max_length=32)
    poster_email = models.EmailField(_('Poster email'), blank=False, help_text=_('Applications will be sent to this address.'))
    apply_online = models.BooleanField(default=True, verbose_name=_('Allow online applications.'),
                                    help_text=_('If you are unchecking this, then add a description on how to apply online!'))
    spotlight = models.BooleanField(_('Spotlight'), default=False)    
    objects = models.Manager()
    active = ActiveJobsManager()
    temporary = TempJobsManager()

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def __unicode__(self):
        return self.title

    def get_application_count(self):
        return JobStat.objects.filter(job=self, stat_type='A').count()
        
    def increment_view_count(self, request):
        lh=last_hour()
        ip=getIP(request)
        hits=JobStat.objects.filter(created_on__range=lh, 
                                        ip=ip, stat_type='H', job=self).count()
        if hits < djobberbase_settings.DJOBBERBASE_MAX_VISITS_PER_HOUR:
            self.views_count=self.views_count+1
            self.save()
            new_hit = JobStat(ip=ip, stat_type='H', job=self)
            new_hit.save()

    def is_active(self):
        return self.status == self.ACTIVE

    def is_temporary(self):
        return self.status == self.TEMPORARY

    def get_status_with_icon(self):
        from django.conf import settings
        icon = '<img src="%(admin_media)simg/admin/%(image)s" alt="%(status)s" /> %(status)s'
        image = {
            self.ACTIVE: 'icon-yes.gif',
            self.TEMPORARY: 'icon-unknown.gif',
            self.INACTIVE: 'icon-no.gif',
        }[self.status]
        return icon % {'admin_media':settings.ADMIN_MEDIA_PREFIX,
                       'image': image,
                       'status': unicode(self.JOB_STATUS_CHOICES[self.status][1])}
    get_status_with_icon.allow_tags = True
    get_status_with_icon.admin_order_field = 'status'
    get_status_with_icon.short_description = 'Status'

    def activate(self):
        self.status = self.ACTIVE
        self.save()

    def deactivate(self):
        self.status = self.INACTIVE
        self.save()

    def email_published_before(self):
        return Job.active.exclude(pk=self.id) \
                          .filter(poster_email=self.poster_email).count() > 0

    @models.permalink
    def get_edit_url(self):
        return ('djobberbase_job_edit', [self.id, self.auth])

    @models.permalink
    def get_absolute_url(self):
        return ('djobberbase_job_detail', [self.id, self.joburl])

    @models.permalink
    def get_activation_url(self):
        return ('djobberbase_job_activate', [self.id, self.auth])		

    @models.permalink
    def get_deactivation_url(self):
        return ('djobberbase_job_deactivate', [self.id, self.auth])

    def clean(self):
        #making sure a job location is selected/typed
        if self.city:
            self.outside_location = ''
        elif len(self.outside_location.strip()) > 0:
            self.city = None
        else:
            raise ValidationError(_('You must select or type a job location.'))

    def save(self, *args, **kwargs):
        #saving auth code
        if not self.auth:
            self.auth = md5(unicode(self.id) + \
                            unicode(uuid.uuid1()) + \
                            unicode(time.time()) ).hexdigest()
        #saving company slug
        self.company_slug = slugify(self.company)

        #saving job url
        self.joburl = slugify(self.title) + \
                        '-' + djobberbase_settings.DJOBBERBASE_AT_URL + \
                        '-' + slugify(self.company)

        #saving with textile
        if djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE == 'textile':
            import textile
            self.description_html = mark_safe(
                                        force_unicode(
                                            textile.textile(
                                                smart_str(self.description))))
        #or markdown
        elif djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE == 'markdown':
            import markdown
            self.description_html = mark_safe(
                                        force_unicode(
                                            markdown.markdown(
                                                smart_str(self.description))))
        else:
            self.description_html = self.description
        super(Job, self).save(*args, **kwargs)
        
class JobStat(models.Model):
    APPLICATION = 'A'
    HIT = 'H'
    SPAM = 'S'
    STAT_TYPES = (
        (APPLICATION, _('Application')),
        (HIT, _('Hit')),
        (SPAM, _('Spam')),
    )
    job = models.ForeignKey(Job)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    ip = models.IPAddressField()
    stat_type = models.CharField(max_length=1, choices=STAT_TYPES)

    class Meta:
        verbose_name = _('Job Stat')
        verbose_name_plural = _('Job Stats')
    
    def __unicode__(self):
        if self.stat_type == 'A':
            u = 'Job application for "' +self.job.title+ '" from IP: '+ self.ip
        elif self.stat_type == 'H':
            u = 'Visit for "' +self.job.title+ '" from IP: ' +self.ip
        elif self.stat_type == 'S':
            u = 'Spam report for "' +self.job.title+ '" from IP: ' + self.ip
        return u
        
class JobSearch(models.Model):
    keywords = models.CharField(_('Keywords'), max_length=100, blank=False)
    created_on = models.DateTimeField(_('Created on'), default=datetime.datetime.now())
    
    class Meta:
        verbose_name = _('Search')
        verbose_name_plural = _('Searches')
    
    def __unicode__(self):
        return self.keywords
