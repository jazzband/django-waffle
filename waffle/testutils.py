from typing import Generic, Optional, TypeVar, Union

from django.test.utils import TestContextDecorator

from waffle import (
    get_waffle_flag_model,
    get_waffle_sample_model,
    get_waffle_switch_model,
)
from waffle.models import Switch, Sample


__all__ = ['override_flag', 'override_sample', 'override_switch']

_T = TypeVar("_T")


class _overrider(TestContextDecorator, Generic[_T]):
    def __init__(self, name: str, active: _T):
        super().__init__()
        self.name = name
        self.active = active

    def get(self) -> None:
        self.obj, self.created = self.cls.objects.get_or_create(name=self.name)

    def update(self, active: _T) -> None:
        raise NotImplementedError

    def get_value(self) -> _T:
        raise NotImplementedError

    def enable(self) -> None:
        self.get()
        self.old_value = self.get_value()
        if self.old_value != self.active:
            self.update(self.active)

    def disable(self) -> None:
        if self.created:
            self.obj.delete()
            self.obj.flush()
        else:
            self.update(self.old_value)


class override_switch(_overrider[bool]):
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
    cls = get_waffle_switch_model()

    def update(self, active: bool) -> None:
        obj = self.cls.objects.get(pk=self.obj.pk)
        obj.active = active
        obj.save()
        obj.flush()

    def get_value(self) -> bool:
        return self.obj.active


class override_flag(_overrider[Optional[bool]]):
    cls = get_waffle_flag_model()

    def update(self, active: Optional[bool]) -> None:
        obj = self.cls.objects.get(pk=self.obj.pk)
        obj.everyone = active
        obj.save()
        obj.flush()

    def get_value(self) -> Optional[bool]:
        return self.obj.everyone


class override_sample(_overrider[Union[bool, float]]):
    cls = get_waffle_sample_model()

    def get(self) -> None:
        try:
            self.obj = self.cls.objects.get(name=self.name)
            self.created = False
        except self.cls.DoesNotExist:
            self.obj = self.cls.objects.create(name=self.name, percent='0.0')
            self.created = True

    def update(self, active: Union[bool, float]) -> None:
        if active is True:
            p = 100.0
        elif active is False:
            p = 0.0
        else:
            p = active
        obj = self.cls.objects.get(pk=self.obj.pk)
        obj.percent = f'{p}'
        obj.save()
        obj.flush()

    def get_value(self) -> Union[bool, float]:
        p = self.obj.percent
        if p == 100.0:
            return True
        if p == 0.0:
            return False
        return p
