# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.sites.models import Site
from django.test import RequestFactory
from django.test.utils import override_settings

from .base import TestCase
from test_app.models import SiteFlag


@override_settings(WAFFLE={'FLAG_CLASS': 'test_app.SiteFlag',
                           'UNIQUE_FLAG_NAME': False})
class SiteFlagTest(TestCase):

    def setUp(self):
        self.site1 = Site(domain='www.example.com')
        self.site1.save()
        self.site2 = Site(domain='www.example.test')
        self.site2.save()

    def tearDown(self):
        models = [SiteFlag, Site]
        for model in models:
            model.objects.all().delete()

    def test_add_flag_to_all_sites(self):
        flag = SiteFlag(site=self.site1, name='test',
                        everyone=True)
        flag.save()
        flag = SiteFlag(site=self.site2, name='test',
                        everyone=True)
        flag.save()
        assert SiteFlag.objects.count() == 2
