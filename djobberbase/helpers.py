# -*- coding: utf-8 -*-

import re
import os
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q
from datetime import datetime, timedelta
from djobberbase.conf import settings as djobberbase_settings

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
        It has been slightly modified from the original to support related fields.    
    '''    
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            if field_name == 'category' or field_name == 'jobtype' or field_name == 'city':
                q = Q(**{"%s__name__icontains" % field_name: term})
            else:
                q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def handle_uploaded_file(f, name):
    file_uploads = djobberbase_settings.DJOBBERBASE_FILE_UPLOADS
    destination = open(file_uploads + name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def delete_uploaded_file(name):
    os.remove(name)

def minutes_between():
    minutes = djobberbase_settings.DJOBBERBASE_MINUTES_BETWEEN
    start = datetime.now() - timedelta(minutes=minutes)
    end = datetime.now()
    return (start, end)
    
def last_hour():
    start = datetime.now() - timedelta(hours=1)
    end = datetime.now()
    return (start, end)
	
def getIP(request):
    ip = request.META['REMOTE_ADDR']    
    if (not ip or ip == '127.0.0.1') and request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    return ip
