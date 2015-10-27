from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

import waffle
from waffle.models import Switch, Flag, Sample
from waffle.testutils import override_switch, override_flag, override_sample


class OverrideSwitchTests(TestCase):
    def test_switch_existed_and_was_active(self):
        Switch.objects.create(name='foo', active=True)

        with override_switch('foo', active=True):
            assert waffle.switch_is_active('foo')

        with override_switch('foo', active=False):
            assert not waffle.switch_is_active('foo')

        # make sure it didn't change 'active' value
        assert Switch.objects.get(name='foo').active

    def test_switch_existed_and_was_NOT_active(self):
        Switch.objects.create(name='foo', active=False)

        with override_switch('foo', active=True):
            assert waffle.switch_is_active('foo')

        with override_switch('foo', active=False):
            assert not waffle.switch_is_active('foo')

        # make sure it didn't change 'active' value
        assert not Switch.objects.get(name='foo').active

    def test_new_switch(self):
        assert not Switch.objects.filter(name='foo').exists()

        with override_switch('foo', active=True):
            assert waffle.switch_is_active('foo')

        with override_switch('foo', active=False):
            assert not waffle.switch_is_active('foo')

        assert not Switch.objects.filter(name='foo').exists()

    def test_as_decorator(self):
        assert not Switch.objects.filter(name='foo').exists()

        @override_switch('foo', active=True)
        def test_enabled():
            assert waffle.switch_is_active('foo')

        test_enabled()

        @override_switch('foo', active=False)
        def test_disabled():
            assert not waffle.switch_is_active('foo')

        test_disabled()

        assert not Switch.objects.filter(name='foo').exists()

    def test_restores_after_exception(self):
        Switch.objects.create(name='foo', active=True)

        def inner():
            with override_switch('foo', active=False):
                raise RuntimeError("Trying to break")

        with self.assertRaises(RuntimeError):
            inner()

        assert Switch.objects.get(name='foo').active

    def test_restores_after_exception_in_decorator(self):
        Switch.objects.create(name='foo', active=True)

        @override_switch('foo', active=False)
        def inner():
            raise RuntimeError("Trying to break")

        with self.assertRaises(RuntimeError):
            inner()

        assert Switch.objects.get(name='foo').active


def req():
    r = RequestFactory().get('/')
    r.user = AnonymousUser()
    return r


class OverrideFlagTests(TestCase):
    def test_flag_existed_and_was_active(self):
        Flag.objects.create(name='foo', everyone=True)

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert Flag.objects.get(name='foo').everyone

    def test_flag_existed_and_was_inactive(self):
        Flag.objects.create(name='foo', everyone=False)

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert Flag.objects.get(name='foo').everyone is False

    def test_flag_existed_and_was_null(self):
        Flag.objects.create(name='foo', everyone=None)

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert Flag.objects.get(name='foo').everyone is None

    def test_flag_did_not_exist(self):
        assert not Flag.objects.filter(name='foo').exists()

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert not Flag.objects.filter(name='foo').exists()


class OverrideSampleTests(TestCase):
    def test_sample_existed_and_was_100(self):
        Sample.objects.create(name='foo', percent='100.0')

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        self.assertEquals(Decimal('100.0'),
                          Sample.objects.get(name='foo').percent)

    def test_sample_existed_and_was_0(self):
        Sample.objects.create(name='foo', percent='0.0')

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        self.assertEquals(Decimal('0.0'),
                          Sample.objects.get(name='foo').percent)

    def test_sample_existed_and_was_50(self):
        Sample.objects.create(name='foo', percent='50.0')

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        self.assertEquals(Decimal('50.0'),
                          Sample.objects.get(name='foo').percent)

    def test_sample_did_not_exist(self):
        assert not Sample.objects.filter(name='foo').exists()

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        assert not Sample.objects.filter(name='foo').exists()


@override_switch('foo', active=False)
class OverrideSwitchOnClassTests(TestCase):
    def setUp(self):
        assert not Switch.objects.filter(name='foo').exists()
        Switch.objects.create(name='foo', active=True)

    def test_undecorated_method_is_set_properly_for_switch(self):
        self.assertFalse(waffle.switch_is_active('foo'))


@override_flag('foo', active=False)
class OverrideFlagOnClassTests(TestCase):
    def setUp(self):
        assert not Flag.objects.filter(name='foo').exists()
        Flag.objects.create(name='foo', everyone=True)

    def test_undecorated_method_is_set_properly_for_flag(self):
        self.assertFalse(waffle.flag_is_active(req(), 'foo'))


@override_sample('foo', active=False)
class OverrideSampleOnClassTests(TestCase):
    def setUp(self):
        assert not Sample.objects.filter(name='foo').exists()
        Sample.objects.create(name='foo', percent='100.0')

    def test_undecorated_method_is_set_properly_for_sample(self):
        self.assertFalse(waffle.sample_is_active('foo'))
