from django.test import TestCase
from waffle.models import Switch
from waffle.testutils import switched
import waffle


class SwitchedTest(TestCase):

    def test_switch_existed_and_was_active(self):
        Switch.objects.create(name='foo', active=True)

        with switched('foo', active=True):
            assert waffle.switch_is_active('foo')

        with switched('foo', active=False):
            assert not waffle.switch_is_active('foo')

        # make sure it didn't change 'active' value
        assert Switch.objects.get(name='foo').active

    def test_switch_existed_and_was_NOT_active(self):
        Switch.objects.create(name='foo', active=False)

        with switched('foo', active=True):
            assert waffle.switch_is_active('foo')

        with switched('foo', active=False):
            assert not waffle.switch_is_active('foo')

        # make sure it didn't change 'active' value
        assert not Switch.objects.get(name='foo').active

    def test_new_switch(self):
        with switched('foo', active=True):
            assert waffle.switch_is_active('foo')

        with switched('foo', active=False):
            assert not waffle.switch_is_active('foo')

        # make sure switch is removed (as it was created inside context manager)
        assert not Switch.objects.filter(name='foo').exists()

    def test_as_decorator(self):

        @switched('foo', active=True)
        def test_enabled():
            assert waffle.switch_is_active('foo')

        test_enabled()

        @switched('foo', active=False)
        def test_disabled():
            assert not waffle.switch_is_active('foo')

        test_disabled()

        # make sure switch is removed (as it was created inside context manager)
        assert not Switch.objects.filter(name='foo').exists()

    def test_restores_after_exception(self):
        Switch.objects.create(name='foo', active=True)

        def inner():
            with switched('foo', active=False):
                raise RuntimeError("Trying to break")

        with self.assertRaises(RuntimeError):
            inner()

        assert Switch.objects.get(name='foo').active

    def test_restores_after_exception_in_decorator(self):
        Switch.objects.create(name='foo', active=True)

        @switched('foo', active=False)
        def inner():
            raise RuntimeError("Trying to break")

        with self.assertRaises(RuntimeError):
            inner()

        assert Switch.objects.get(name='foo').active

