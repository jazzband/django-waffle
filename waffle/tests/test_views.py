from django.urls import reverse

from waffle import (
    get_waffle_flag_model,
    get_waffle_sample_model,
    get_waffle_switch_model,
)
from waffle.tests.base import TestCase


class WaffleViewTests(TestCase):
    def test_wafflejs(self):
        response = self.client.get(reverse('wafflejs'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/x-javascript', response['content-type'])
        cache_control = [control.strip()
                         for control in response['cache-control'].split(',')]
        self.assertIn('max-age=0', cache_control)

    def test_waffle_status(self):
        response = self.client.get(reverse('waffle_status'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response['content-type'])
        cache_control = [control.strip()
                         for control in response['cache-control'].split(',')]
        self.assertIn('max-age=0', cache_control)

    def test_waffle_status_response(self):
        get_waffle_flag_model().objects.create(name='test_flag_active', everyone=True)
        get_waffle_flag_model().objects.create(name='test_flag_inactive', everyone=False)
        get_waffle_switch_model().objects.create(name='test_switch_active', active=True)
        get_waffle_switch_model().objects.create(name='test_switch_inactive', active=False)
        get_waffle_sample_model().objects.create(name='test_sample_active', percent=100)
        get_waffle_sample_model().objects.create(name='test_sample_inactive', percent=0)

        response = self.client.get(reverse('waffle_status'))
        self.assertEqual(200, response.status_code)
        content = response.json()

        assert 'test_flag_active' in content['flags'].keys()
        assert content['flags']['test_flag_active']['is_active']
        assert 'test_flag_inactive' in content['flags'].keys()
        assert not content['flags']['test_flag_inactive']['is_active']

        assert 'test_switch_active' in content['switches'].keys()
        assert content['switches']['test_switch_active']['is_active']
        assert 'test_switch_inactive' in content['switches'].keys()
        assert not content['switches']['test_switch_inactive']['is_active']

        assert 'test_sample_active' in content['samples'].keys()
        assert content['samples']['test_sample_active']['is_active']
        assert 'test_sample_inactive' in content['samples'].keys()
        assert not content['samples']['test_sample_inactive']['is_active']

    def test_flush_all_flags(self):
        """Test the 'FLAGS_ALL' list gets invalidated correctly."""
        get_waffle_flag_model().objects.create(name='myflag1', everyone=True)
        response = self.client.get(reverse('wafflejs'))
        self.assertEqual(200, response.status_code)
        assert ('myflag1', True) in response.context['flags']

        get_waffle_flag_model().objects.create(name='myflag2', everyone=True)
        response = self.client.get(reverse('wafflejs'))
        self.assertEqual(200, response.status_code)
        assert ('myflag2', True) in response.context['flags']

    def test_flush_all_switches(self):
        """Test the 'SWITCHES_ALL' list gets invalidated correctly."""
        switch = get_waffle_switch_model().objects.create(name='myswitch', active=True)
        response = self.client.get(reverse('wafflejs'))
        self.assertEqual(200, response.status_code)
        assert ('myswitch', True) in response.context['switches']

        switch.active = False
        switch.save()
        response = self.client.get(reverse('wafflejs'))
        self.assertEqual(200, response.status_code)
        assert ('myswitch', False) in response.context['switches']

    def test_flush_all_samples(self):
        """Test the 'SAMPLES_ALL' list gets invalidated correctly."""
        get_waffle_sample_model().objects.create(name='sample1', percent='100.0')
        response = self.client.get(reverse('wafflejs'))
        self.assertEqual(200, response.status_code)
        assert ('sample1', True) in response.context['samples']

        get_waffle_sample_model().objects.create(name='sample2', percent='100.0')

        response = self.client.get(reverse('wafflejs'))
        self.assertEqual(200, response.status_code)
        assert ('sample2', True) in response.context['samples']
