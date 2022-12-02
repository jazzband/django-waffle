import contextlib
import random
from decimal import Decimal
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.test import RequestFactory, TestCase, TransactionTestCase

import waffle
from waffle.testutils import override_flag, override_sample, override_switch


class OverrideSwitchMixin:
    def test_switch_existed_and_was_active(self):
        waffle.get_waffle_switch_model().objects.create(name='foo', active=True)

        with override_switch('foo', active=True):
            assert waffle.switch_is_active('foo')

        with override_switch('foo', active=False):
            assert not waffle.switch_is_active('foo')

        # make sure it didn't change 'active' value
        assert waffle.get_waffle_switch_model().objects.get(name='foo').active

    def test_switch_existed_and_was_NOT_active(self):
        waffle.get_waffle_switch_model().objects.create(name='foo', active=False)

        with override_switch('foo', active=True):
            assert waffle.switch_is_active('foo')

        with override_switch('foo', active=False):
            assert not waffle.switch_is_active('foo')

        # make sure it didn't change 'active' value
        assert not waffle.get_waffle_switch_model().objects.get(name='foo').active

    def test_new_switch(self):
        assert not waffle.get_waffle_switch_model().objects.filter(name='foo').exists()

        with override_switch('foo', active=True):
            assert waffle.switch_is_active('foo')

        with override_switch('foo', active=False):
            assert not waffle.switch_is_active('foo')

        assert not waffle.get_waffle_switch_model().objects.filter(name='foo').exists()

    def test_as_decorator(self):
        assert not waffle.get_waffle_switch_model().objects.filter(name='foo').exists()

        @override_switch('foo', active=True)
        def test_enabled():
            assert waffle.switch_is_active('foo')

        test_enabled()

        @override_switch('foo', active=False)
        def test_disabled():
            assert not waffle.switch_is_active('foo')

        test_disabled()

        assert not waffle.get_waffle_switch_model().objects.filter(name='foo').exists()

    def test_restores_after_exception(self):
        waffle.get_waffle_switch_model().objects.create(name='foo', active=True)

        def inner():
            with override_switch('foo', active=False):
                raise RuntimeError("Trying to break")

        with self.assertRaises(RuntimeError):
            inner()

        assert waffle.get_waffle_switch_model().objects.get(name='foo').active

    def test_restores_after_exception_in_decorator(self):
        waffle.get_waffle_switch_model().objects.create(name='foo', active=True)

        @override_switch('foo', active=False)
        def inner():
            raise RuntimeError("Trying to break")

        with self.assertRaises(RuntimeError):
            inner()

        assert waffle.get_waffle_switch_model().objects.get(name='foo').active

    def test_cache_is_flushed_by_testutils_even_in_transaction(self):
        waffle.get_waffle_switch_model().objects.create(name='foo', active=True)

        with transaction.atomic():
            with override_switch('foo', active=True):
                assert waffle.switch_is_active('foo')

            with override_switch('foo', active=False):
                assert not waffle.switch_is_active('foo')

        assert waffle.switch_is_active('foo')


class OverrideSwitchTestCase(OverrideSwitchMixin, TestCase):
    """
    Run tests with Django TestCase
    """


class OverrideSwitchTransactionTestCase(OverrideSwitchMixin, TransactionTestCase):
    """
    Run tests with Django TransactionTestCase
    """


def req():
    r = RequestFactory().get('/')
    r.user = AnonymousUser()
    return r


@contextlib.contextmanager
def provide_user(**kwargs):
    user = get_user_model()(**kwargs)
    user.save()
    yield user
    user.delete()


class OverrideFlagTestsMixin:
    def test_flag_existed_and_was_active(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=True)

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').everyone

    def test_flag_existed_and_was_inactive(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=False)

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').everyone is False

    def test_flag_existed_and_was_null(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None)

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').everyone is None

    def test_flag_did_not_exist(self):
        assert not waffle.get_waffle_flag_model().objects.filter(name='foo').exists()

        with override_flag('foo', active=True):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', active=False):
            assert not waffle.flag_is_active(req(), 'foo')

        assert not waffle.get_waffle_flag_model().objects.filter(name='foo').exists()

    def test_cache_is_flushed_by_testutils_even_in_transaction(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=True)

        with transaction.atomic():
            with override_flag('foo', active=True):
                assert waffle.flag_is_active(req(), 'foo')

            with override_flag('foo', active=False):
                assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.flag_is_active(req(), 'foo')

    @mock.patch.object(random, 'uniform')
    def test_flag_existed_and_was_active_for_percent(self, uniform):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, percent='50')

        uniform.return_value = '75'

        with override_flag('foo', percent=80.0):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', percent=40.0):
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').percent == Decimal('50')

    @mock.patch.object(random, 'uniform')
    def test_flag_existed_and_was_inactive_for_percent(self, uniform):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, percent=None)

        uniform.return_value = '75'

        with override_flag('foo', percent=80.0):
            assert waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', percent=40.0):
            assert not waffle.flag_is_active(req(), 'foo')

        assert not waffle.get_waffle_flag_model().objects.get(name='foo').percent

    def test_flag_existed_and_was_active_for_testing(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, testing=True)

        with override_flag('foo', testing=True):
            request = req()
            request.COOKIES['dwft_foo'] = 'True'
            assert waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', testing=False):
            request = req()
            request.COOKIES['dwft_foo'] = 'True'
            assert not waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').testing

    def test_flag_existed_and_was_inactive_for_testing(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, testing=False)

        with override_flag('foo', testing=True):
            request = req()
            request.COOKIES['dwft_foo'] = 'True'
            assert waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', testing=False):
            request = req()
            request.COOKIES['dwft_foo'] = 'True'
            assert not waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        assert not waffle.get_waffle_flag_model().objects.get(name='foo').testing

    def test_flag_existed_and_was_active_for_superusers(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, superusers=True)

        with override_flag('foo', superusers=True):
            with provide_user(username='foo', is_superuser=True) as user:
                request = req()
                request.user = user
                assert waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_superuser=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        with override_flag('foo', superusers=False):
            with provide_user(username='foo', is_superuser=True) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_superuser=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').superusers

    def test_flag_existed_and_was_inactive_for_superusers(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, superusers=False)

        with override_flag('foo', superusers=True):
            with provide_user(username='foo', is_superuser=True) as user:
                request = req()
                request.user = user
                assert waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_superuser=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        with override_flag('foo', superusers=False):
            with provide_user(username='foo', is_superuser=True) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_superuser=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        assert not waffle.get_waffle_flag_model().objects.get(name='foo').superusers

    def test_flag_existed_and_was_active_for_staff(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, staff=True)

        with override_flag('foo', staff=True):
            with provide_user(username='foo', is_staff=True) as user:
                request = req()
                request.user = user
                assert waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_staff=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        with override_flag('foo', staff=False):
            with provide_user(username='foo', is_staff=True) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_staff=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').staff

    def test_flag_existed_and_was_inactive_for_staff(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, staff=False)

        with override_flag('foo', staff=True):
            with provide_user(username='foo', is_staff=True) as user:
                request = req()
                request.user = user
                assert waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_staff=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        with override_flag('foo', staff=False):
            with provide_user(username='foo', is_staff=True) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')
            with provide_user(username='foo', is_staff=False) as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')

        assert not waffle.get_waffle_flag_model().objects.get(name='foo').staff

    def test_flag_existed_and_was_active_for_authenticated(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, authenticated=True)

        with override_flag('foo', authenticated=True):
            with provide_user(username='foo') as user:
                request = req()
                request.user = user
                assert waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', authenticated=False):
            with provide_user(username='foo') as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').authenticated

    def test_flag_existed_and_was_inactive_for_authenticated(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, authenticated=False)

        with override_flag('foo', authenticated=True):
            with provide_user(username='foo') as user:
                request = req()
                request.user = user
                assert waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', authenticated=False):
            with provide_user(username='foo') as user:
                request = req()
                request.user = user
                assert not waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        assert not waffle.get_waffle_flag_model().objects.get(name='foo').authenticated

    def test_flag_existed_and_was_active_for_languages(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, languages="en,es")

        with override_flag('foo', languages="en,es"):
            request = req()
            request.LANGUAGE_CODE = "en"
            assert waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', languages=""):
            request = req()
            request.LANGUAGE_CODE = "en"
            assert not waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').languages == "en,es"

    def test_flag_existed_and_was_inactive_for_languages(self):
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=None, languages="")

        with override_flag('foo', languages="en,es"):
            request = req()
            request.LANGUAGE_CODE = "en"
            assert waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        with override_flag('foo', languages=""):
            request = req()
            request.LANGUAGE_CODE = "en"
            assert not waffle.flag_is_active(request, 'foo')
            assert not waffle.flag_is_active(req(), 'foo')

        assert waffle.get_waffle_flag_model().objects.get(name='foo').languages == ""


class OverrideFlagsTestCase(OverrideFlagTestsMixin, TestCase):
    """
    Run tests with Django TestCase
    """


class OverrideFlagsTransactionTestCase(OverrideFlagTestsMixin, TransactionTestCase):
    """
    Run tests with Django TransactionTestCase
    """


class OverrideSampleTestsMixin:
    def test_sample_existed_and_was_100(self):
        waffle.get_waffle_sample_model().objects.create(name='foo', percent='100.0')

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        self.assertEqual(Decimal('100.0'),
                         waffle.get_waffle_sample_model().objects.get(name='foo').percent)

    def test_sample_existed_and_was_0(self):
        waffle.get_waffle_sample_model().objects.create(name='foo', percent='0.0')

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        self.assertEqual(Decimal('0.0'),
                         waffle.get_waffle_sample_model().objects.get(name='foo').percent)

    def test_sample_existed_and_was_50(self):
        waffle.get_waffle_sample_model().objects.create(name='foo', percent='50.0')

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        self.assertEqual(Decimal('50.0'),
                         waffle.get_waffle_sample_model().objects.get(name='foo').percent)

    def test_sample_did_not_exist(self):
        assert not waffle.get_waffle_sample_model().objects.filter(name='foo').exists()

        with override_sample('foo', active=True):
            assert waffle.sample_is_active('foo')

        with override_sample('foo', active=False):
            assert not waffle.sample_is_active('foo')

        assert not waffle.get_waffle_sample_model().objects.filter(name='foo').exists()

    def test_cache_is_flushed_by_testutils_even_in_transaction(self):
        waffle.get_waffle_sample_model().objects.create(name='foo', percent='100.0')

        with transaction.atomic():
            with override_sample('foo', active=True):
                assert waffle.sample_is_active('foo')

            with override_sample('foo', active=False):
                assert not waffle.sample_is_active('foo')

        assert waffle.sample_is_active('foo')


class OverrideSampleTestCase(OverrideSampleTestsMixin, TestCase):
    """
    Run tests with Django TestCase
    """


class OverrideSampleTransactionTestCase(OverrideSampleTestsMixin, TransactionTestCase):
    """
    Run tests with Django TransactionTestCase
    """


class OverrideSwitchOnClassTestsMixin:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        assert not waffle.get_waffle_switch_model().objects.filter(name='foo').exists()
        waffle.get_waffle_switch_model().objects.create(name='foo', active=True)

    def test_undecorated_method_is_set_properly_for_switch(self):
        self.assertFalse(waffle.switch_is_active('foo'))


@override_switch('foo', active=False)
class OverrideSwitchOnClassTestCase(OverrideSwitchOnClassTestsMixin,
                                    TestCase):
    """
    Run tests with Django TestCase
    """


@override_switch('foo', active=False)
class OverrideSwitchOnClassTransactionTestCase(OverrideSwitchOnClassTestsMixin,
                                               TransactionTestCase):
    """
    Run tests with Django TransactionTestCase
    """


class OverrideFlagOnClassTestsMixin:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        assert not waffle.get_waffle_flag_model().objects.filter(name='foo').exists()
        waffle.get_waffle_flag_model().objects.create(name='foo', everyone=True)

    def test_undecorated_method_is_set_properly_for_flag(self):
        self.assertFalse(waffle.flag_is_active(req(), 'foo'))


@override_flag('foo', active=False)
class OverrideFlagOnClassTestCase(OverrideFlagOnClassTestsMixin,
                                  TestCase):
    """
    Run tests with Django TestCase
    """


@override_flag('foo', active=False)
class OverrideFlagOnClassTransactionTestCase(OverrideFlagOnClassTestsMixin,
                                             TransactionTestCase):
    """
    Run tests with Django TransactionTestCase
    """


class OverrideSampleOnClassTestsMixin:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        assert not waffle.get_waffle_sample_model().objects.filter(name='foo').exists()
        waffle.get_waffle_sample_model().objects.create(name='foo', percent='100.0')

    def test_undecorated_method_is_set_properly_for_sample(self):
        self.assertFalse(waffle.sample_is_active('foo'))


@override_sample('foo', active=False)
class OverrideSampleOnClassTestCase(OverrideSampleOnClassTestsMixin,
                                    TestCase):
    """
    Run tests with Django TestCase
    """


@override_sample('foo', active=False)
class OverrideSampleOnClassTransactionTestCase(OverrideSampleOnClassTestsMixin,
                                               TransactionTestCase):
    """
    Run tests with Django TransactionTestCase
    """


class InheritanceOverrideSwitchOnClassTests(OverrideSwitchOnClassTestCase):
    """
    Extend ``OverrideSwitchOnClassTestCase``
    and make sure ``override_switch`` change still works.
    """

    def test_child_undecorated_method_is_set_properly_for_switch(self):
        self.assertFalse(waffle.switch_is_active('foo'))


class InheritanceOverrideFlagOnClassTests(OverrideFlagOnClassTestCase):
    """
    Extend ``OverrideFlagOnClassTestCase``
    and make sure ``override_flag`` change still works.
    """

    def test_child_undecorated_method_is_set_properly_for_flag(self):
        self.assertFalse(waffle.flag_is_active(req(), 'foo'))


class InheritanceOverrideSampleOnClassTests(OverrideSampleOnClassTestCase):
    """
    Extend ``OverrideSampleOnClassTestCase``
    and make sure ``override_sample`` change still works.
    """

    def test_child_undecorated_method_is_set_properly_for_sample(self):
        self.assertFalse(waffle.sample_is_active('foo'))
