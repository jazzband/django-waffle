from __future__ import unicode_literals

import six
from django.core.management import call_command
from django.contrib.auth.models import Group

from waffle.models import Flag, Sample, Switch
from waffle.tests.base import TestCase


class WaffleFlagManagementCommandTests(TestCase):
    def test_create(self):
        """ The command should create a new flag. """
        name = 'test'
        percent = 20
        Group.objects.create(name='waffle_group')
        call_command('waffle_flag', name, everyone=True, percent=percent,
                     superusers=True, staff=True, authenticated=True,
                     rollout=True, create=True, group=['waffle_group'])

        flag = Flag.objects.get(name=name)
        self.assertEqual(flag.percent, percent)
        self.assertTrue(flag.everyone)
        self.assertTrue(flag.superusers)
        self.assertTrue(flag.staff)
        self.assertTrue(flag.authenticated)
        self.assertTrue(flag.rollout)
        self.assertEqual(list(flag.groups.values_list('name', flat=True)),
                         ['waffle_group'])

    def test_update(self):
        """ The command should update an existing flag. """
        name = 'test'
        flag = Flag.objects.create(name=name)
        self.assertIsNone(flag.percent)
        self.assertIsNone(flag.everyone)
        self.assertTrue(flag.superusers)
        self.assertFalse(flag.staff)
        self.assertFalse(flag.authenticated)
        self.assertFalse(flag.rollout)

        percent = 30
        call_command('waffle_flag', name, everyone=True, percent=percent,
                     superusers=False, staff=True, authenticated=True,
                     rollout=True)

        flag.refresh_from_db()
        self.assertEqual(flag.percent, percent)
        self.assertTrue(flag.everyone)
        self.assertFalse(flag.superusers)
        self.assertTrue(flag.staff)
        self.assertTrue(flag.authenticated)
        self.assertTrue(flag.rollout)

    def test_list(self):
        """ The command should list all flags."""
        stdout = six.StringIO()
        Flag.objects.create(name='test')

        call_command('waffle_flag', list_flags=True, stdout=stdout)
        expected = 'Flags:\nNAME: test\nSUPERUSERS: True\nEVERYONE: None\n' \
                   'AUTHENTICATED: False\nPERCENT: None\nTESTING: False\n' \
                   'ROLLOUT: False\nSTAFF: False\nGROUPS: []'
        actual = stdout.getvalue().strip()
        self.assertEqual(actual, expected)

    def test_group_append(self):
        """ The command should append a group to a flag. """
        original_group = Group.objects.create(name='waffle_group')
        Group.objects.create(name='append_group')
        flag = Flag.objects.create(name='test')
        flag.groups.add(original_group)
        flag.refresh_from_db()

        self.assertEqual(list(flag.groups.values_list('name', flat=True)),
                         ['waffle_group'])

        call_command('waffle_flag', 'test', group=['append_group'],
                     append=True)

        flag.refresh_from_db()
        self.assertEqual(list(flag.groups.values_list('name', flat=True)),
                         ['waffle_group', 'append_group'])


class WaffleSampleManagementCommandTests(TestCase):
    def test_create(self):
        """ The command should create a new sample. """
        name = 'test'
        percent = 20
        call_command('waffle_sample', name, str(percent), create=True)

        sample = Sample.objects.get(name=name)
        self.assertEqual(sample.percent, percent)

    def test_update(self):
        """ The command should update an existing sample. """
        name = 'test'
        sample = Sample.objects.create(name=name, percent=0)
        self.assertEqual(sample.percent, 0)

        percent = 50
        call_command('waffle_sample', name, str(percent))

        sample.refresh_from_db()
        self.assertEqual(sample.percent, percent)

    def test_list(self):
        """ The command should list all samples."""
        stdout = six.StringIO()
        Sample.objects.create(name='test', percent=34)

        call_command('waffle_sample', list_samples=True, stdout=stdout)
        expected = 'Samples:\ntest: 34.0%'
        actual = stdout.getvalue().strip()
        self.assertEqual(actual, expected)


class WaffleSwitchManagementCommandTests(TestCase):
    def test_create(self):
        """ The command should create a new switch. """
        name = 'test'

        call_command('waffle_switch', name, 'on', create=True)
        switch = Switch.objects.get(name=name, active=True)
        switch.delete()

        call_command('waffle_switch', name, 'off', create=True)
        Switch.objects.get(name=name, active=False)

    def test_update(self):
        """ The command should update an existing switch. """
        name = 'test'
        switch = Switch.objects.create(name=name, active=True)

        call_command('waffle_switch', name, 'off')
        switch.refresh_from_db()
        self.assertFalse(switch.active)

        call_command('waffle_switch', name, 'on')
        switch.refresh_from_db()
        self.assertTrue(switch.active)

    def test_list(self):
        """ The command should list all switches."""
        stdout = six.StringIO()
        Switch.objects.create(name='switch1', active=True)
        Switch.objects.create(name='switch2', active=False)

        call_command('waffle_switch', list_switches=True, stdout=stdout)
        expected = 'Switches:\nswitch1: on\nswitch2: off'
        actual = stdout.getvalue().strip()
        self.assertEqual(actual, expected)
