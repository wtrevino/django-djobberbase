# -*- coding: utf-8 -*-

import os
import re
from django.conf import settings
from django.core.validators import email_re
from django.core.exceptions import ImproperlyConfigured

# General settings
SIMPLEADS_SITE_NAME = getattr(settings, 'SIMPLEADS_SITE_NAME', 'Djobberbase')
SIMPLEADS_HTML_TITLE = getattr(settings, 'SIMPLEADS_HTML_TITLE', 'Djobberbase :: A jobberBase clone written using the Django framework')
SIMPLEADS_SITE_KEYWORDS = getattr(settings, 'SIMPLEADS_SITE_KEYWORDS', ('job search', 'jobs', 'employment'))
SIMPLEADS_SITE_DESCRIPTION = getattr(settings, 'SIMPLEADS_SITE_DESCRIPTION', 'Djobberbase jobs.')
SIMPLEADS_MINUTES_BETWEEN = getattr(settings, 'SIMPLEADS_MINUTES_BETWEEN', 10)
SIMPLEADS_MAX_UPLOAD_SIZE = getattr(settings, 'SIMPLEADS_MAX_UPLOAD_SIZE', 3145728)
SIMPLEADS_FILE_UPLOADS = getattr(settings, 'SIMPLEADS_FILE_UPLOADS', './uploads/')
SIMPLEADS_JOBS_PER_PAGE = getattr(settings, 'SIMPLEADS_JOBS_PER_PAGE', 50)
SIMPLEADS_JOBS_PER_SEARCH = getattr(settings, 'SIMPLEADS_JOBS_PER_SEARCH', 25)
SIMPLEADS_MAX_VISITS_PER_HOUR = getattr(settings, 'SIMPLEADS_MAX_VISITS_PER_HOUR', 1)
SIMPLEADS_CAPTCHA_POST = getattr(settings, 'SIMPLEADS_CAPTCHA_POST', None)
SIMPLEADS_CAPTCHA_APPLICATION = getattr(settings, 'SIMPLEADS_CAPTCHA_APPLICATION', None)
SIMPLEADS_CV_EXTENSIONS = getattr(settings, 'SIMPLEADS_CV_EXTENSIONS', ('pdf', 'rtf', 'doc', 'docx', 'odt'))

# Custom URLs settings
def geturl(url_set, url, default):
    ''' It checks if the url is valid and not already in use, in case
        it's an invalid url then the default url is returned.
    '''
    u = getattr(settings, url, default)
    if re.match("^[a-zA-Z0-9_.-]+$", u) is not None and u not in url_set:
        url_set.append(u)
    else:
        raise ImproperlyConfigured('The url "%s" is already in use' % u)
    return u

url_set = []
SIMPLEADS_POST_URL = geturl(url_set, 'SIMPLEADS_POST_URL', 'post')
SIMPLEADS_VERIFY_URL = geturl(url_set, 'SIMPLEADS_VERIFY_URL', 'verify')
SIMPLEADS_CONFIRM_URL = geturl(url_set, 'SIMPLEADS_CONFIRM_URL', 'confirm')
SIMPLEADS_JOB_URL = geturl(url_set, 'SIMPLEADS_JOB_URL', 'job')
SIMPLEADS_AT_URL = geturl(url_set, 'SIMPLEADS_AT_URL', 'at')
SIMPLEADS_JOBS_URL = geturl(url_set, 'SIMPLEADS_JOBS_URL', 'jobs')
SIMPLEADS_CITIES_URL = geturl(url_set, 'SIMPLEADS_CITIES_URL', 'cities')
SIMPLEADS_COMPANIES_URL = geturl(url_set, 'SIMPLEADS_COMPANIES_URL', 'companies')
SIMPLEADS_JOBS_IN_URL = geturl(url_set, 'SIMPLEADS_JOBS_IN_URL', 'jobs-in')
SIMPLEADS_JOBS_IN_OTHER_CITIES_URL = geturl(url_set, 'SIMPLEADS_JOBS_IN_OTHER_CITIES_URL', 'jobs-in-other-cities')
SIMPLEADS_JOBS_AT_URL = geturl(url_set, 'SIMPLEADS_JOBS_AT_URL', 'jobs-at')
SIMPLEADS_ACTIVATE_URL = geturl(url_set, 'SIMPLEADS_ACTIVATE_URL', 'activate')
SIMPLEADS_DEACTIVATE_URL = geturl(url_set, 'SIMPLEADS_DEACTIVATE_URL', 'deactivate')
SIMPLEADS_SEARCH_URL = geturl(url_set, 'SIMPLEADS_SEARCH_URL', 'search')
SIMPLEADS_UNAVAILABLE_URL = geturl(url_set, 'SIMPLEADS_UNAVAILABLE_URL', 'job-unavailable')

# Mailing settings
SIMPLEADS_ENABLE_NEW_POST_MODERATION = getattr(settings, 'SIMPLEADS_ENABLE_NEW_POST_MODERATION', True)
SIMPLEADS_ADMIN_EMAIL = getattr(settings, 'SIMPLEADS_ADMIN_EMAIL', '')
SIMPLEADS_ADMIN_NOTIFICATIONS = getattr(settings, 'SIMPLEADS_ADMIN_NOTIFICATIONS', False)
SIMPLEADS_POSTER_NOTIFICATIONS = getattr(settings, 'SIMPLEADS_POSTER_NOTIFICATIONS', False)
SIMPLEADS_APPLICATION_NOTIFICATIONS = getattr(settings, 'SIMPLEADS_APPLICATION_NOTIFICATIONS', False)

SIMPLEADS_NEW_POST_ADMIN_SUBJECT = getattr(settings, 
                                    'SIMPLEADS_NEW_POST_ADMIN_SUBJECT', 
                                    '[ %(site_name)s  ] New job: %(job_title)s')

SIMPLEADS_EDIT_POST_ADMIN_SUBJECT = getattr(settings, 
                                    'SIMPLEADS_EDIT_POST_ADMIN_SUBJECT', 
                                    '[ %(site_name)s  ] Edited job: %(job_title)s')

SIMPLEADS_MAIL_PENDING_SUBJECT = getattr(settings, 
                                    'SIMPLEADS_MAIL_PENDING_SUBJECT', 
                                    'Your ad on %(site_name)s')

SIMPLEADS_MAIL_PUBLISH_SUBJECT = getattr(settings, 
                                    'SIMPLEADS_MAIL_PUBLISH_SUBJECT', 
                                    'Your ad on %(site_name)s was published')
 
SIMPLEADS_MAIL_APPLY_ONLINE_SUBJECT = getattr(settings, 
                                    'SIMPLEADS_MAIL_APPLY_ONLINE_SUBJECT', 
                                    '[ %(site_name)s ] I wish to apply for %(job_title)s')


# Markup settings
SIMPLEADS_MARKUP_LANGUAGE = getattr(settings, 'SIMPLEADS_MARKUP_LANGUAGE', None) #options: 'textile', 'markdown'

