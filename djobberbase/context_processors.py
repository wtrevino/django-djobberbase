# -*- coding: utf-8 -*-

from djobberbase.conf import settings
from djobberbase.models import Job, Type

def general_settings(request):
    tv = {}
    tv['DJOBBERBASE_SITE_NAME'] = settings.DJOBBERBASE_SITE_NAME
    tv['DJOBBERBASE_HTML_TITLE'] = settings.DJOBBERBASE_HTML_TITLE 
    tv['DJOBBERBASE_SITE_KEYWORDS'] = settings.DJOBBERBASE_SITE_KEYWORDS
    tv['DJOBBERBASE_SITE_DESCRIPTION'] = settings.DJOBBERBASE_SITE_DESCRIPTION
    return tv

def categories_and_types(request):
    tv = {}
    tv['djobberbase_categories'] = Category.objects.all().order_by('category_order')
    tv['djobberbase_types'] = Type.objects.all()
    
