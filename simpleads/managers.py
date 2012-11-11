# -*- coding: utf-8 -*-
from django.contrib.sites.managers import CurrentSiteManager


class TempJobsManager(CurrentSiteManager):
    def get_query_set(self):
        return super(TempJobsManager, self).get_query_set() \
                        .filter(status=self.model.TEMPORARY)


class ActiveJobsManager(CurrentSiteManager):
    def get_query_set(self):
        return super(ActiveJobsManager, self).get_query_set() \
                        .filter(status=self.model.ACTIVE)
