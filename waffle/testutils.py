from __future__ import unicode_literals

import sys
import types
from functools import wraps

from waffle.models import Flag, Switch, Sample


__all__ = ['override_flag', 'override_sample', 'override_switch']
PY3 = sys.version_info[0] == 3
if PY3:
    CLASS_TYPES = (type,)
else:
    CLASS_TYPES = (type, types.ClassType)


class _overrider(object):
    def __init__(self, name, active):
        self.name = name
        self.active = active

    def __call__(self, func):
        if isinstance(func, CLASS_TYPES):
            return self.for_class(func)
        else:
            return self.for_callable(func)

    def for_class(self, obj):
        """Wraps a class's test methods in the decorator"""
        for attr in dir(obj):
            if not attr.startswith('test_'):
                # Ignore non-test functions
                continue

            attr_value = getattr(obj, attr)

            if not callable(attr_value):
                # Ignore non-functions
                continue

            setattr(obj, attr, self.for_callable(attr_value))

        return obj

    def for_callable(self, func):
        """Wraps a method in the decorator"""
        @wraps(func)
        def _wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return _wrapped

    def get(self):
        self.obj, self.created = self.cls.objects.get_or_create(name=self.name)

    def update(self, active):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def __enter__(self):
        self.get()
        self.old_value = self.get_value()
        if self.old_value != self.active:
            self.update(self.active)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.created:
            self.obj.delete()
        else:
            self.update(self.old_value)


class override_switch(_overrider):
    """
    override_switch is a contextmanager for easier testing of switches.

    It accepts two parameters, name of the switch and it's state. Example
    usage::

        with override_switch('happy_mode', active=True):
            ...

    If `Switch` already existed, it's value would be changed inside the context
    block, then restored to the original value. If `Switch` did not exist
    before entering the context, it is created, then removed at the end of the
    block.

    It can also act as a decorator::

        @override_switch('happy_mode', active=True)
        def test_happy_mode_enabled():
            ...

    """
    cls = Switch

    def update(self, active):
        obj = self.cls.objects.get(pk=self.obj.pk)
        obj.active = active
        obj.save()

    def get_value(self):
        return self.obj.active


class override_flag(_overrider):
    cls = Flag

    def update(self, active):
        obj = self.cls.objects.get(pk=self.obj.pk)
        obj.everyone = active
        obj.save()

    def get_value(self):
        return self.obj.everyone


class override_sample(_overrider):
    cls = Sample

    def get(self):
        try:
            self.obj = self.cls.objects.get(name=self.name)
            self.created = False
        except self.cls.DoesNotExist:
            self.obj = self.cls.objects.create(name=self.name, percent='0.0')
            self.created = True

    def update(self, active):
        if active is True:
            p = 100.0
        elif active is False:
            p = 0.0
        else:
            p = active
        obj = self.cls.objects.get(pk=self.obj.pk)
        obj.percent = '{0}'.format(p)
        obj.save()

    def get_value(self):
        p = self.obj.percent
        if p == 100.0:
            return True
        if p == 0.0:
            return False
        return p
