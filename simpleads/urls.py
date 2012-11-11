# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from simpleads.models import Job, Category, Type, City
from simpleads.conf import settings as simpleads_settings
from simpleads.feeds import LatestJobsFeed

if simpleads_settings.SIMPLEADS_CAPTCHA_POST == 'simple':
    from simpleads.forms import CaptchaJobForm
    form_class = CaptchaJobForm
else:
    from simpleads.forms import JobForm
    form_class = JobForm


urlpatterns = patterns('django.views.generic',

    #An index view
    url(r'^$',
        'list_detail.object_list', 
        { 'queryset': Job.active.all(),          
          'extra_context': {'page_type': 'index'},
          'paginate_by': simpleads_settings.SIMPLEADS_JOBS_PER_PAGE},
        name='simpleads_job_list'),
    
    #Cities view    
    url(r'^'+simpleads_settings.SIMPLEADS_CITIES_URL+'/$',
        'list_detail.object_list', 
        { 'queryset': City.objects.all(),
          'extra_context': {'page_type': 'cities', 
                    'other_cities_total': Job.active.filter(city=None).count}},
        name='simpleads_cities_list'),

    #post new job
    url(r'^'+simpleads_settings.SIMPLEADS_POST_URL+'/$',
        'create_update.create_object', 
        { 'form_class': form_class, 
          'post_save_redirect': '../'+
          simpleads_settings.SIMPLEADS_VERIFY_URL+'/%(id)d/%(auth)s/'},
        name='simpleads_job_post'),

    #job unavailable
    url(r'^'+simpleads_settings.SIMPLEADS_UNAVAILABLE_URL+'/$',
        'simple.direct_to_template', 
        {'template': 'simpleads/unavailable.html'},
        name='simpleads_job_unavailable'),
)

urlpatterns += patterns('',

    #verify job
    url(r'^'+simpleads_settings.SIMPLEADS_VERIFY_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'simpleads.views.job_verify', 
        name='simpleads_job_verify'),

    #all jobs
    url(r'^'+simpleads_settings.SIMPLEADS_JOBS_URL+'/$',
        'simpleads.views.jobs_category',
        name='simpleads_job_list_all'),

    #all jobs with category
    url(r'^'+simpleads_settings.SIMPLEADS_JOBS_URL+
        '/(?P<cvar_name>[-\w]+)/$',
        'simpleads.views.jobs_category',
        name='simpleads_job_list_category'),

    #all jobs with category and job type    
    url(r'^'+simpleads_settings.SIMPLEADS_JOBS_URL+
        '/(?P<cvar_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'simpleads.views.jobs_category',
        name='simpleads_job_list_category_type'),

    #Job detail    
    url(r'^'+simpleads_settings.SIMPLEADS_JOB_URL+
        '/(?P<job_id>\d+)/(?P<joburl>[-\w]+)/$',
        'simpleads.views.job_detail',
        name='simpleads_job_detail'),
        
    #Jobs in city view
    url(r'^'+simpleads_settings.SIMPLEADS_JOBS_IN_URL+
        '/(?P<city_name>[-\w]+)/$',
        'simpleads.views.jobs_in_city',
        name='simpleads_jobs_in_city'),

    #Jobs in other cities
    url(r'^'+simpleads_settings.SIMPLEADS_JOBS_IN_OTHER_CITIES_URL+'/$',
        'simpleads.views.jobs_in_other_cities',
        name='simpleads_jobs_in_other_cities'),

    #Jobs in city+jobtype view
    url(r'^'+simpleads_settings.SIMPLEADS_JOBS_IN_URL+
        '/(?P<city_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'simpleads.views.jobs_in_city',
        name='simpleads_jobs_in_city_jobtype'),

    #Companies
    url(r'^'+simpleads_settings.SIMPLEADS_COMPANIES_URL+'/$',
        'simpleads.views.companies',
        name='simpleads_companies'),

    #Jobs at (company)
    url(r'^'+simpleads_settings.SIMPLEADS_JOBS_AT_URL+
        '/(?P<company_slug>[-\w]+)/$',
        'simpleads.views.jobs_at',
        name='simpleads_jobs_at'),

    #Job confirm
    url(r'^'+simpleads_settings.SIMPLEADS_CONFIRM_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'simpleads.views.job_confirm',
        name='simpleads_job_confirm'),

    #Edit job
    url(r'^'+simpleads_settings.SIMPLEADS_POST_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'simpleads.views.job_edit',
        name='simpleads_job_edit'),

    #Activate job
    url(r'^'+simpleads_settings.SIMPLEADS_ACTIVATE_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'simpleads.views.job_activate',
        name='simpleads_job_activate'),

    #Deactivate job
    url(r'^'+simpleads_settings.SIMPLEADS_DEACTIVATE_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'simpleads.views.job_deactivate',
        name='simpleads_job_deactivate'),

    #Search
    url(r'^'+simpleads_settings.SIMPLEADS_SEARCH_URL+'/$',
        'simpleads.views.job_search',
        name='simpleads_job_search'),

    #Feed
    url(r'^rss/(?P<var_name>[-\w]+)/$',
        LatestJobsFeed(),
        name='simpleads_feed'),

)
