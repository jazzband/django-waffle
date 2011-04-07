from nose.tools import eq_
from test_utils import TestCase

from waffle.models import Flag, Switch


class DecoratorTests(TestCase):
    def test_flag_must_be_active(self):
        resp = self.client.get('/flag-on')
        eq_(404, resp.status_code)
        Flag.objects.create(name='foo', everyone=True)
        resp = self.client.get('/flag-on')
        eq_(200, resp.status_code)

    def test_flag_must_be_inactive(self):
        resp = self.client.get('/flag-off')
        eq_(200, resp.status_code)
        Flag.objects.create(name='foo', everyone=True)
        resp = self.client.get('/flag-off')
        eq_(404, resp.status_code)

    def test_switch_must_be_active(self):
        resp = self.client.get('/switch-on')
        eq_(404, resp.status_code)
        Switch.objects.create(name='foo', active=True)
        resp = self.client.get('/switch-on')
        eq_(200, resp.status_code)

    def test_switch_must_be_inactive(self):
        resp = self.client.get('/switch-off')
        eq_(200, resp.status_code)
        Switch.objects.create(name='foo', active=True)
        resp = self.client.get('/switch-off')
        eq_(404, resp.status_code)
