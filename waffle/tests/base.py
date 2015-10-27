from __future__ import unicode_literals

from django import test
from django.core import cache


class TestCase(test.TransactionTestCase):

    def _pre_setup(self):
        cache.cache.clear()
        super(TestCase, self)._pre_setup()
