# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, render_to_response
from djobberbase.models import Job, Category, Type, JobStat, JobSearch, City
from djobberbase.postman import *
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import create_object, update_object
from django.core.context_processors import csrf
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from djobberbase.helpers import *
from djobberbase.forms import ApplicationForm, JobForm
from djobberbase.conf import settings as djobberbase_settings
from django.db.models import Count
from django.http import Http404

def job_detail(request, job_id, joburl):
    ''' Displays an active job and its application form depending if 
        the job has online applications or not. Handles the job applications
        and sends notifications emails.
    '''
    try:        
        job = Job.active.get(pk=job_id, joburl=joburl)
        extra_context = {'page_type':'detail', 
               'cv_extensions': djobberbase_settings.DJOBBERBASE_CV_EXTENSIONS,
               'markup_lang': djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE}

        # Increment views
        job.increment_view_count(request)

        # Gets poster ip
        ip = getIP(request)

        # Only if the job has online applications ON and application 
        # notifications are activated can the user apply online
        mb = minutes_between()
        if job.apply_online and djobberbase_settings.\
            DJOBBERBASE_APPLICATION_NOTIFICATIONS:

            # Add CSRF protection
            extra_context.update(csrf(request))

            # If it's a job application
            if request.method == 'POST':

                # Gets the application
                form = ApplicationForm(request.POST, 
                                       request.FILES, 
                                       applicant_data={'ip':ip, 'mb':mb})

                # If the form is OK then send it to the job poster
                if form.is_valid():
                    application_mail = MailApplyOnline(job, request)
                    application_mail.start()

                    #Save JobStat application
                    ja = JobStat(job=job, ip=ip, stat_type='A')
                    ja.save()
                    messages.add_message(request, 
                                messages.INFO, 
                                _('Your application was sent successfully.'))
                    extra_context['page_type'] = 'application'
                    queryset = Job.active.filter(joburl=joburl)
                    return object_detail(request, queryset=queryset,
                                        object_id=job_id,
                                        extra_context=extra_context)
                else:
                    extra_context['form_error'] = True 

            # Else create an empty application form
            else:
                form = ApplicationForm(applicant_data={'ip':ip, 'mb':mb})
            extra_context['apform'] = form
            extra_context['object'] = job
            return render_to_response('djobberbase/job_detail.html',
                                       extra_context,
                                       context_instance=RequestContext(request))

        # Only display the job, without an application form
        else:
            queryset = Job.active.filter(joburl=joburl)
            return object_detail(request, queryset=queryset,
                                object_id=job_id,
                                extra_context=extra_context)

    # Instead of throwing a 404 error redirect to job unavailable page 
    except Job.DoesNotExist:
        return redirect('djobberbase_job_unavailable', permanent=True)

def job_verify(request, job_id, auth):
    ''' A view to display a newly created job.
    '''
    queryset = Job.objects.filter(auth=auth)
    # Setting page_type as 'verify' in order to 
    # show edit and cancelation buttons in the template
    extra_context = {'page_type':'verify', 
               'markup_lang': djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE}
    return object_detail(request, queryset=queryset, 
                            object_id=job_id, extra_context=extra_context)

def jobs_category(request, cvar_name=None, tvar_name=None):
    ''' Displays a job list by category and/or job type but
        those two are optional.
    '''
    extra_context = {}
    queryset = Job.active.all()
    if cvar_name:
        category = get_object_or_404(Category, var_name=cvar_name)
        queryset = queryset.filter(category=category)
        extra_context['selected_category'] = category
    if tvar_name:
        jobtype = get_object_or_404(Type, var_name=tvar_name)
        queryset = queryset.filter(jobtype=jobtype)
        extra_context['selected_jobtype'] = jobtype
    return object_list(request, queryset=queryset,
                    extra_context=extra_context,
                    paginate_by=djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE)

def jobs_in_city(request, city_name, tvar_name=None):
    ''' Display a job list by city and job type (optional).
    '''
    city = get_object_or_404(City, ascii_name=city_name)
    queryset = Job.active.filter(city=city)
    extra_context = {'city': city}
    if tvar_name:
        jobtype = get_object_or_404(Type, var_name=tvar_name)
        queryset = queryset.filter(jobtype=jobtype)
        extra_context['selected_jobtype'] = jobtype                     
    return object_list(request, queryset=queryset,
                    extra_context=extra_context,
                    paginate_by=djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE)

def jobs_in_other_cities(request):
    ''' Displays a list with jobs in cities outside.
    '''
    queryset = Job.active.filter(city=None)
    return object_list(request, queryset=queryset)

def companies(request):
    ''' Displays the companies that have active jobs
        posted on the site.
    '''
    queryset = Job.active.values('company', 'company_slug') \
               .annotate(Count('company'))
    return object_list(request, queryset=queryset,
                                template_name='djobberbase/company_list.html')

def jobs_at(request, company_slug, tvar_name=None):
    ''' Displays a job list by company, jobtype is optional.
    '''
    queryset = Job.active.filter(company_slug=company_slug)
    if tvar_name:
        jobtype = get_object_or_404(Type, var_name=tvar_name)
        queryset = queryset.filter(jobtype=jobtype)
        extra_context['selected_jobtype'] = jobtype    
    return object_list(request, queryset=queryset)

def job_confirm(request, job_id, auth):
    ''' A view to confirm a recently created job, if it has been published
        by a previously approved user then it gets automatically published,
        if not then it will need to be verified by a moderator.
    '''
    job = get_object_or_404(Job, pk=job_id, auth=auth)
    if job.status not in (Job.ACTIVE, Job.TEMPORARY):
        raise Http404
    new_post = job.is_temporary()
    requires_mod = not job.email_published_before() and \
                 djobberbase_settings.DJOBBERBASE_ENABLE_NEW_POST_MODERATION
    if requires_mod:
        messages.add_message(request, 
                       messages.INFO, 
                       _('Your job post needs to be verified by a moderator.'))
        if djobberbase_settings.DJOBBERBASE_POSTER_NOTIFICATIONS:
            pending_email = MailPublishPendingToUser(job, request)
            pending_email.start()
    else:
        messages.add_message(request, 
                             messages.INFO, 
                             _('Your job post has been published.'))
        if not job.is_active():
            job.activate()
        if new_post:
            if djobberbase_settings.DJOBBERBASE_POSTER_NOTIFICATIONS:
                publish_email = MailPublishToUser(job, request)
                publish_email.start()    
    queryset = Job.objects.all()
    if djobberbase_settings.DJOBBERBASE_ADMIN_NOTIFICATIONS:
        admin_email = MailPublishToAdmin(job, request)
        admin_email.start()
    return object_detail(request, queryset=queryset,
                         object_id=job_id,
                         extra_context={'page_type':'confirm'})
                         
def job_edit(request, job_id, auth):
    ''' A view for editing published or unpublished job posts.
    '''
    job = get_object_or_404(Job, pk=job_id, auth=auth)
    if job.status not in (Job.ACTIVE, Job.TEMPORARY):
        raise Http404
    return update_object(request, form_class=JobForm, object_id=job_id,
           post_save_redirect='../../../'+
           djobberbase_settings.DJOBBERBASE_VERIFY_URL+'/%(id)d/%(auth)s/')

def job_activate(request, job_id, auth):
    ''' Gets a job and activates it, only if it's not already activated,
        it also sends the notification mail to the poster.
    '''
    job = get_object_or_404(Job, pk=job_id, auth=auth)
    extra_context={}
    if not job.is_active():
        job.activate()
        if djobberbase_settings.DJOBBERBASE_POSTER_NOTIFICATIONS:
            publish_email = MailPublishToUser(job, request)
            publish_email.start()
        messages.add_message(request, 
                             messages.INFO, 
                             _('Your job has been activated.'))
        extra_context['page_type'] = 'activate'
    queryset=Job.active.all()
    return object_detail(request, queryset=queryset, 
                            object_id=job_id, extra_context=extra_context)

def job_deactivate(request, job_id, auth):
    ''' Deactivates a job and shows an active jobs list.    
    '''
    job = get_object_or_404(Job, pk=job_id, auth=auth)
    extra_context={}
    if job.is_active() or job.is_temporary():
        job.deactivate()
        messages.add_message(request, 
                             messages.INFO, 
                             _('Your job has been deactivated.'))
        extra_context['page_type'] = 'deactivate'
    queryset=Job.active.all()
    return object_list(request, queryset=queryset,
                    extra_context=extra_context,
                    paginate_by=djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE)

def job_search(request):
    ''' A search view, does the job but not great. Job searches should be
        handled by a proper search app, namely django-haystack.
    '''
    query_string = ''
    found_entries = Job.objects.none()
    extra_context = {'keywords': ' '}
    if ('keywords' in request.POST) and request.POST['keywords'].strip():
        request.session['keywords'] = request.POST['keywords']
        query_string = request.session['keywords']
        extra_context['keywords'] = query_string
        search_fields = ['title', 'description', 'category',
                             'jobtype', 'city', 'outside_location', 'company',]
        entry_query = get_query(query_string, search_fields)
        jobs_per_search = djobberbase_settings.DJOBBERBASE_JOBS_PER_SEARCH
        found_entries = Job.objects.filter(entry_query)\
                                     .order_by('-created_on')[:jobs_per_search]
        search = JobSearch(keywords=query_string)
        search.save()
    return object_list(request, queryset=found_entries,
                    extra_context=extra_context,
                    paginate_by=djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE)
