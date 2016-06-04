# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.db import models
from django.contrib.sites.models import Site
from waffle.models import BaseFlag


class Flag(BaseFlag):

    class Meta:
        abstract = False


class SiteFlag(BaseFlag):

    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        abstract = False
        unique_together = (('name', 'site'),)
