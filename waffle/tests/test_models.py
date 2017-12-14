from django.contrib.auth.models import User, AnonymousUser

from waffle.models import Flag
from waffle.tests.base import TestCase


class FlagTests(TestCase):
    def test_is_active_for_user(self):
        flag = Flag.objects.create(name='foo', authenticated=True)
        user = User.objects.create(username='foo')
        assert flag.is_active_for_user(user)

        user = AnonymousUser()
        assert not flag.is_active_for_user(user)
