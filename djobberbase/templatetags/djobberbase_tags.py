# -*- coding: utf-8 -*-

from django import template
from djobberbase.models import Job, Category, Type, JobStat
from django.utils.safestring import mark_safe
from django.db.models import Count
import re

# latest jobs template tag
def do_latest_jobs(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_latest_jobs' tag takes exactly four arguments")    
    return LatestJobsNode(bits[1], bits[3])

class LatestJobsNode(template.Node):
    def __init__(self, num, varname):
        self.num = int(num)
        self.varname = varname

    def render(self, context):
        context[self.varname] = Job.active.all().order_by('-created_on')[:self.num]
        return ''

# spotlight jobs template tag
def do_spotlight_jobs(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_spotlight_jobs' tag takes exactly four arguments")
    return SpotlightJobsNode(bits[1], bits[3])

class SpotlightJobsNode(template.Node):
    def __init__(self, num, varname):
        self.num = int(num)
        self.varname = varname

    def render(self, context):
        context[self.varname] = Job.active.filter(spotlight=True).order_by('-created_on')[:self.num]
        return ''

#most applied jobs template tag
def do_most_applied_jobs(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_most_applied_jobs' tag takes exactly four arguments")
    return MostAppliedJobsNode(bits[1], bits[3])

class MostAppliedJobsNode(template.Node):
    def __init__(self, num, varname):
        self.num = int(num)
        self.varname = varname

    def render(self, context):
        applications = JobStat.objects.filter(stat_type='A').values('job').annotate(Count('job')).order_by('-job__count')[:self.num]
        jobs = []
        for application in applications:
            jobs.append(Job.active.get(pk=application['job']))
        context[self.varname] = jobs
        return ''


# categories template tag
def do_categories(parser, token):
    return CategoriesNode()

class CategoriesNode(template.Node):
    def render(self, context):
        context['total_jobs'] = Job.active.all().count()
        context['categories'] = Category.objects.all().order_by('category_order')
        return ''

def do_jobtypes(parser, token):
    return JobtypesNode()

class JobtypesNode(template.Node):
    def render(self, context):
        context['jobtypes'] = Type.objects.all()
        return ''

NOFOLLOW_RE = re.compile(u'<a (?![^>]*rel=["\']nofollow[\'"])' \
                         u'(?![^>]*href=["\']\.{0,2}/[^/])',
                         re.UNICODE|re.IGNORECASE)
def nofollow(content):
    return mark_safe(re.sub(NOFOLLOW_RE, u'<a rel="nofollow" ', content))

register = template.Library()
register.tag('get_latest_jobs', do_latest_jobs)
register.tag('get_spotlight_jobs', do_spotlight_jobs)
register.tag('get_most_applied_jobs', do_most_applied_jobs)
register.tag('get_categories', do_categories)
register.tag('get_jobtypes', do_jobtypes)
register.filter(nofollow)
