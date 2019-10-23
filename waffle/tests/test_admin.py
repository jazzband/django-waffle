from __future__ import unicode_literals
try:
    import mock
except ImportError:
    import unittest.mock as mock

from django.contrib.admin.models import LogEntry, CHANGE, DELETION
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from waffle import get_waffle_flag_model
from waffle.admin import (FlagAdmin, InformativeManyToManyRawIdWidget, enable_for_all,
                          disable_for_all, delete_individually, enable_switches, disable_switches)
from waffle.models import Switch
from waffle.tests.base import TestCase


class FakeSuperUser:
    def has_perm(self, perm):
        return True


class FakeRequest:
    def __init__(self):
        self.user = get_user_model().objects.create(username="test1")


Flag = get_waffle_flag_model()


class FlagAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_informative_widget(self):
        flag_admin = FlagAdmin(Flag, self.site)

        request = mock.Mock()
        request.has_perm = lambda self, perm: True
        form = flag_admin.get_form(request)()
        user_widget = form.fields["users"].widget

        self.assertIsInstance(user_widget, InformativeManyToManyRawIdWidget)
        user1 = get_user_model().objects.create(username="test1")
        user2 = get_user_model().objects.create(username="test2")
        self.assertIn("(test1, test2)",
                      user_widget.render("users", [user1.pk, user2.pk]))

    def test_enable_for_all(self):
        f1 = Flag.objects.create(name="flag1", everyone=False)

        request = FakeRequest()
        enable_for_all(None, request, Flag.objects.all())

        f1.refresh_from_db()
        self.assertTrue(f1.everyone)
        log_entry = LogEntry.objects.get(user=request.user)
        self.assertEqual(log_entry.action_flag, CHANGE)
        self.assertEqual(log_entry.object_repr, "flag1 on")

    def test_disable_for_all(self):
        f1 = Flag.objects.create(name="flag1", everyone=True)

        request = FakeRequest()
        disable_for_all(None, request, Flag.objects.all())

        f1.refresh_from_db()
        self.assertFalse(f1.everyone)
        log_entry = LogEntry.objects.get(user=request.user)
        self.assertEqual(log_entry.action_flag, CHANGE)
        self.assertEqual(log_entry.object_repr, "flag1 off")

    def test_delete_individually(self):
        Flag.objects.create(name="flag1", everyone=True)

        request = FakeRequest()
        delete_individually(None, request, Flag.objects.all())

        self.assertIsNone(Flag.objects.first())
        log_entry = LogEntry.objects.get(user=request.user)
        self.assertEqual(log_entry.action_flag, DELETION)

    def test_enable_switches(self):
        s1 = Switch.objects.create(name="switch1", active=False)

        request = FakeRequest()
        enable_switches(None, request, Switch.objects.all())

        s1.refresh_from_db()
        self.assertTrue(s1.active)
        log_entry = LogEntry.objects.get(user=request.user)
        self.assertEqual(log_entry.action_flag, CHANGE)
        self.assertEqual(log_entry.object_repr, "switch1 on")

    def test_disable_switches(self):
        s1 = Switch.objects.create(name="switch1", active=True)

        request = FakeRequest()
        disable_switches(None, request, Switch.objects.all())

        s1.refresh_from_db()
        self.assertFalse(s1.active)
        log_entry = LogEntry.objects.get(user=request.user)
        self.assertEqual(log_entry.action_flag, CHANGE)
        self.assertEqual(log_entry.object_repr, "switch1 off")
