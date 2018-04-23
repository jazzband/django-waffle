from __future__ import unicode_literals

import mock
from django.test import RequestFactory
from waffle.tests.base import TestCase
from waffle import waffle_flag_call, waffle_switch_call
from waffle.callables import WaffleCallable


class WaffleFlagCallTests(TestCase):

    def setUp(self):
        self.active_callable = WaffleCallable(mock.MagicMock())
        self.inactive_callable = WaffleCallable(mock.MagicMock())
        factory = RequestFactory()
        self.request = factory.get('/any/url')

    @mock.patch('waffle.flag_is_active', return_value=True)
    def test_waffle_flag_call_calls_active_callable_if_flag_active_without_exclamation(
            self, flag_is_active):
            
        waffle_flag_call(
            self.request, 'fake_flag', self.active_callable, 
            self.inactive_callable)

        flag_is_active.assert_called_once_with(self.request, 'fake_flag')
        self.active_callable.func.assert_called_once_with()
        self.inactive_callable.func.assert_not_called()

    @mock.patch('waffle.flag_is_active', return_value=False)
    def test_waffle_flag_call_calls_inactive_callable_if_flag_inactive_without_exclamation(
            self, flag_is_active):
            
        waffle_flag_call(
            self.request, 'fake_flag', self.active_callable, 
            self.inactive_callable)

        flag_is_active.assert_called_once_with(self.request, 'fake_flag')
        self.active_callable.func.assert_not_called()
        self.inactive_callable.func.assert_called_once_with()
        
    @mock.patch('waffle.flag_is_active', return_value=True)
    def test_waffle_flag_call_calls_active_callable_if_flag_active_with_exclamation(
            self, flag_is_active):
        waffle_flag_call(
            self.request, '!fake_flag', self.active_callable, 
            self.inactive_callable)

        flag_is_active.assert_called_once_with(self.request, 'fake_flag')
        self.active_callable.func.assert_not_called()
        self.inactive_callable.func.assert_called_once_with()

    @mock.patch('waffle.flag_is_active', return_value=False)
    def test_waffle_flag_call_calls_active_callable_if_flag_inactive_with_exclamation(
            self, flag_is_active):
        waffle_flag_call(
            self.request, '!fake_flag', self.active_callable, 
            self.inactive_callable)

        flag_is_active.assert_called_once_with(self.request, 'fake_flag')
        self.active_callable.func.assert_called_once_with()
        self.inactive_callable.func.assert_not_called()
        
    def test_call_waffle_flag_call_with_not_WaffleCallable_active_callable(self):
        with self.assertRaises(AssertionError):
            waffle_flag_call(
                self.request, '!fake_flag', None,
                self.inactive_callable)

    def test_call_waffle_flag_call_with_not_none_or_WaffleCallable_inactive_callable(self):
        with self.assertRaises(AssertionError):
            waffle_flag_call(
                self.request, '!fake_flag', self.active_callable,
                'test')


class WaffleSwitchCallTests(TestCase):

    def setUp(self):
        self.active_callable = WaffleCallable(mock.MagicMock())
        self.inactive_callable = WaffleCallable(mock.MagicMock())
        factory = RequestFactory()
        self.request = factory.get('/any/url')

    @mock.patch('waffle.switch_is_active', return_value=True)
    def test_waffle_switch_call_calls_active_callable_if_switch_active_without_exclamation(
            self, switch_is_active):
            
        waffle_switch_call(
            'fake_switch', self.active_callable, self.inactive_callable)

        switch_is_active.assert_called_once_with('fake_switch')
        self.active_callable.func.assert_called_once_with()
        self.inactive_callable.func.assert_not_called()

    @mock.patch('waffle.switch_is_active', return_value=False)
    def test_waffle_switch_call_calls_inactive_callable_if_switch_inactive_without_exclamation(
            self, switch_is_active):
            
        waffle_switch_call(
            'fake_switch', self.active_callable, self.inactive_callable)

        switch_is_active.assert_called_once_with('fake_switch')
        self.active_callable.func.assert_not_called()
        self.inactive_callable.func.assert_called_once_with()
        
    @mock.patch('waffle.switch_is_active', return_value=True)
    def test_waffle_switch_call_calls_active_callable_if_switch_active_with_exclamation(
            self, switch_is_active):
        waffle_switch_call(
            '!fake_switch', self.active_callable, self.inactive_callable)

        switch_is_active.assert_called_once_with('fake_switch')
        self.active_callable.func.assert_not_called()
        self.inactive_callable.func.assert_called_once_with()

    @mock.patch('waffle.switch_is_active', return_value=False)
    def test_waffle_switch_call_calls_active_callable_if_switch_inactive_with_exclamation(
            self, switch_is_active):
        waffle_switch_call(
            '!fake_switch', self.active_callable, 
            self.inactive_callable)

        switch_is_active.assert_called_once_with('fake_switch')
        self.active_callable.func.assert_called_once_with()
        self.inactive_callable.func.assert_not_called()
        
    def test_call_waffle_switch_call_with_not_WaffleCallable_active_callable(self):
        with self.assertRaises(AssertionError):
            waffle_switch_call(
                '!fake_switch', None, self.inactive_callable)

    def test_call_waffle_switch_call_with_not_none_or_WaffleCallable_inactive_callable(self):
        with self.assertRaises(AssertionError):
            waffle_switch_call(
                '!fake_switch', self.active_callable, 'test')
