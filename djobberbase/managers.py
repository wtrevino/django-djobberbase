# -*- coding: utf-8 -*-

from django.db import models

class TempJobsManager(models.Manager):
    def get_query_set(self):
        return super(TempJobsManager, self).get_query_set() \
                        .filter(status=self.model.TEMPORARY)

class ActiveJobsManager(models.Manager):
    def get_query_set(self):
        return super(ActiveJobsManager, self).get_query_set() \
                        .filter(status=self.model.ACTIVE)
