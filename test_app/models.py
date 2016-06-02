# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from waffle.models import BaseFlag


class Flag(BaseFlag):

    class Meta:
        abstract = False
