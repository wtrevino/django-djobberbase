# -*- coding: utf-8 -*-

from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site
from djobberbase.helpers import getIP, handle_uploaded_file, delete_uploaded_file
from djobberbase.conf import settings as djobberbase_settings
from time import time
import threading

site_domain = Site.objects.get_current().domain

class MailPublishToAdmin(threading.Thread):

    def __init__(self, job, request):
        threading.Thread.__init__(self)
        plaintext = get_template('djobberbase/emails/publish_to_admin.txt')
        html = get_template('djobberbase/emails/publish_to_admin.html')
        template_vars = {}
        template_vars['job_url'] = 'http://%s%s' % (site_domain, job.get_absolute_url())
        template_vars['job_title'] = job.title
        template_vars['job_company'] = job.company
        template_vars['job_description'] = job.description
        template_vars['job_poster_email'] = job.poster_email
        job_info = {
                    'site_name': djobberbase_settings.DJOBBERBASE_SITE_NAME,
                    'job_title': job.title,
        }
        subject = djobberbase_settings.DJOBBERBASE_EDIT_POST_ADMIN_SUBJECT % job_info
        if not job.is_active():
            subject = djobberbase_settings.DJOBBERBASE_NEW_POST_ADMIN_SUBJECT % job_info
            template_vars['job_activate_url'] = 'http://%s%s' % (site_domain, job.get_activation_url())
        template_vars['job_edit_url'] = 'http://%s%s' % (site_domain, job.get_edit_url())
        template_vars['job_deactivate_url'] = 'http://%s%s' % (site_domain, job.get_deactivation_url())
        template_vars['job_poster_ip'] = getIP(request)
        template_vars['job_post_date'] = job.created_on
        d = Context(template_vars)

        from_email = djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL
        to = djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL
        text_content = plaintext.render(d)
        html_content = html.render(d)
        self.email = EmailMultiAlternatives(subject, text_content, from_email, [to])
        self.email.attach_alternative(html_content, "text/html")

    def run(self):
        self.email.send()

class MailPublishPendingToUser(threading.Thread):

    def __init__(self, job, request):
        threading.Thread.__init__(self)
        plaintext = get_template('djobberbase/emails/publish_pending_to_user.txt')
        html = get_template('djobberbase/emails/publish_pending_to_user.html')
        template_vars = {}
        template_vars['job_url'] = 'http://%s%s' % (site_domain, job.get_absolute_url())
        template_vars['job_title'] = job.title
        template_vars['job_company'] = job.company
        template_vars['job_description'] = job.description
        template_vars['job_poster_email'] = job.poster_email
        template_vars['job_post_date'] = job.created_on
        d = Context(template_vars)
        job_info = {
                    'site_name': djobberbase_settings.DJOBBERBASE_SITE_NAME,
                    'job_title': job.title,
        }
        subject = djobberbase_settings.DJOBBERBASE_MAIL_PENDING_SUBJECT %  job_info
        from_email = djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL
        to = job.poster_email
        text_content = plaintext.render(d)
        html_content = html.render(d)
        self.email = EmailMultiAlternatives(subject, text_content, from_email, [to])
        self.email.attach_alternative(html_content, "text/html")

    def run(self):
        self.email.send()

class MailPublishToUser(threading.Thread):

    def __init__(self, job, request):
        threading.Thread.__init__(self)
        plaintext = get_template('djobberbase/emails/publish_to_user.txt')
        html = get_template('djobberbase/emails/publish_to_user.html')
        template_vars = {}
        template_vars['job_url'] = 'http://%s%s' % (site_domain, job.get_absolute_url())
        template_vars['job_edit_url'] = 'http://%s%s' % (site_domain, job.get_edit_url())
        template_vars['job_deactivate_url'] = 'http://%s%s' % (site_domain, job.get_deactivation_url())
        template_vars['site_name'] = djobberbase_settings.DJOBBERBASE_SITE_NAME
        d = Context(template_vars)
        job_info = {
                    'site_name': djobberbase_settings.DJOBBERBASE_SITE_NAME,
                    'job_title': job.title,
        }
        subject = djobberbase_settings.DJOBBERBASE_MAIL_PUBLISH_SUBJECT % job_info 
        from_email = djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL
        to = job.poster_email
        text_content = plaintext.render(d)
        html_content = html.render(d)
        self.email = EmailMultiAlternatives(subject, text_content, from_email, [to])
        self.email.attach_alternative(html_content, "text/html")

    def run(self):
        self.email.send()

class MailApplyOnline(threading.Thread):

    def __init__(self, job, request):
        threading.Thread.__init__(self)
        job_info = {
                    'site_name': djobberbase_settings.DJOBBERBASE_SITE_NAME,
                    'job_title': job.title,
        }
        subject = djobberbase_settings.DJOBBERBASE_MAIL_APPLY_ONLINE_SUBJECT % job_info
        from_email = djobberbase_settings.DJOBBERBASE_ADMIN_EMAIL
        to = job.poster_email
        msg = request.POST['apply_msg']
        self.email = EmailMessage(subject, msg, from_email, [to], headers = {'Reply-To': request.POST['apply_email']})
        if 'apply_cv' in request.FILES.keys():
            name = unicode(int(time()))+'_'+request.FILES['apply_cv'].name
            handle_uploaded_file(request.FILES['apply_cv'], name)
            self.email.attach_file(djobberbase_settings.DJOBBERBASE_FILE_UPLOADS + name)
            delete_uploaded_file(djobberbase_settings.DJOBBERBASE_FILE_UPLOADS + name)

    def run(self):
        self.email.send()
