from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model

from test_app.models import Flag
from waffle.admin import FlagAdmin, InformativeManyToManyRawIdWidget
from waffle.tests.base import TestCase
from waffle.utils import get_flag_model, get_setting

try:
    import mock
except ImportError:
    import unittest.mock as mock



class FakeSuperUser:
    def has_perm(self, perm):
        return True


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
