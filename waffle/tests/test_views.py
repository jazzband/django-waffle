from django.core.urlresolvers import reverse

from nose.tools import eq_
from test_utils import TestCase


class WaffleViewTests(TestCase):
    def test_wafflejs(self):
        response = self.client.get(reverse('wafflejs'))
        eq_(200, response.status_code)
        eq_('application/x-javascript', response['content-type'])
        eq_('max-age=0', response['cache-control'])
