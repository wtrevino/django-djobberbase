# -*- coding: utf-8 -*-

from simpleads.conf import settings
from simpleads.models import Job, Type

def general_settings(request):
    tv = {}
    tv['SIMPLEADS_SITE_NAME'] = settings.SIMPLEADS_SITE_NAME
    tv['SIMPLEADS_HTML_TITLE'] = settings.SIMPLEADS_HTML_TITLE 
    tv['SIMPLEADS_SITE_KEYWORDS'] = settings.SIMPLEADS_SITE_KEYWORDS
    tv['SIMPLEADS_SITE_DESCRIPTION'] = settings.SIMPLEADS_SITE_DESCRIPTION
    return tv

def categories_and_types(request):
    tv = {}
    tv['simpleads_categories'] = Category.on_site.all().order_by('category_order')
    tv['simpleads_types'] = Type.on_site.all()
    
