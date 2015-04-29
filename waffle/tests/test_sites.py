from django.db import connection
from django.contrib.sites.models import Site
from django.contrib.auth.models import AnonymousUser, Group, User

import waffle
from waffle.models import Flag, Sample, Switch
from waffle.tests.base import TestCase

from test_app import views

from waffle.tests.test_waffle import get, process_request


class SiteTests(TestCase):
    def setUp(self):
        super(SiteTests, self).setUp()
        Site.objects.create(domain='example2.com', name='example2.com')

        self.site1 = Site.objects.get(name='example.com')
        self.site2 = Site.objects.get(name='example2.com')

    def test_switch_by_site(self):
        """ test that we can get different switch values by site """
        name = 'myswitch'
        switch1 = Switch.objects.create(name=name, active=True, site=self.site1)
        switch2 = Switch.objects.create(name=name, active=False, site=self.site2)

        self.assertTrue(waffle.switch_is_active(name))

        with self.settings(SITE_ID=2):
            self.assertFalse(waffle.switch_is_active(name))

    def test_switch_site_default(self):
        name = 'myswitch'
        switch = Switch.objects.create(name=name, active=True) # no site given

        self.assertTrue(waffle.switch_is_active(name))

        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.switch_is_active(name))

    def test_sample_by_site(self):
        name = 'sample'
        sample1 = Sample.objects.create(name=name, percent='100.0', site=self.site1)
        sample2 = Sample.objects.create(name=name, percent='0.0', site=self.site2)

        self.assertTrue(waffle.sample_is_active(name))

        with self.settings(SITE_ID=2):
            self.assertFalse(waffle.sample_is_active(name))

    def test_sample_site_default(self):
        name = 'sample'
        sample = Sample.objects.create(name=name, percent='100.0') # no site given

        self.assertTrue(waffle.sample_is_active(name))

        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.sample_is_active(name))

    def test_flag_by_site(self):
        name = 'myflag'
        flag1 = Flag.objects.create(name=name, everyone=True, site=self.site1)
        flag2 = Flag.objects.create(name=name, everyone=False, site=self.site2)
        request = get()

        response = process_request(request, views.flag_in_view)
        self.assertContains(response, b'on')

        with self.settings(SITE_ID=2):
            response = process_request(request, views.flag_in_view)
            self.assertContains(response, b'off')
