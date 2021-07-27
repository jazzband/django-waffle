# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _

from waffle.models import CACHE_EMPTY, AbstractUserFlag, BaseFlag
from waffle.utils import get_cache, get_setting, keyfmt

cache = get_cache()


class Flag(BaseFlag):

    class Meta:
        abstract = False


class SiteFlag(BaseFlag):

    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        abstract = False
        unique_together = (('name', 'site'),)
