from waffle.models import Flag, Switch
from waffle.tests.base import TestCase


class DecoratorTests(TestCase):
    def test_flag_must_be_active(self):
        resp = self.client.get('/flag-on')
        self.assertEqual(404, resp.status_code)
        Flag.objects.create(name='foo', everyone=True)
        resp = self.client.get('/flag-on')
        self.assertEqual(200, resp.status_code)

    def test_flag_must_be_inactive(self):
        resp = self.client.get('/flag-off')
        self.assertEqual(200, resp.status_code)
        Flag.objects.create(name='foo', everyone=True)
        resp = self.client.get('/flag-off')
        self.assertEqual(404, resp.status_code)

    def test_switch_must_be_active(self):
        resp = self.client.get('/switch-on')
        self.assertEqual(404, resp.status_code)
        Switch.objects.create(name='foo', active=True)
        resp = self.client.get('/switch-on')
        self.assertEqual(200, resp.status_code)

    def test_switch_must_be_inactive(self):
        resp = self.client.get('/switch-off')
        self.assertEqual(200, resp.status_code)
        Switch.objects.create(name='foo', active=True)
        resp = self.client.get('/switch-off')
        self.assertEqual(404, resp.status_code)
