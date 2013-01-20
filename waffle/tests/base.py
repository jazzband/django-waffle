from django.test import Client

from test_utils import TestCase as BaseTestCase


class TestCase(BaseTestCase):
    def setUp(self):
        super(TestCase, self).setUp()

        self.client = Client()
