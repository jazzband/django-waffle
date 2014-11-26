from waffle.models import Switch


class switched(object):
    """
    switched is a context manager for easier integration testing of switches.

    It accepts two parameters, name of the switch and it's state. Example
    usage::

        with switched('happy_mode', active=True):
            ...

    If `Switch` already existed, it's value would be changed inside the context
    block, then restored to the original value. If `Switch` did not exist
    before entering the context, it is created, then removed at the end of the
    block.

    It can also act as a decorator::

        @switched('happy_mode', active=True)
        def test_happy_mode_enabled():
            ...

    """
    def __init__(self, name, active):
        self.name = name
        self.active = active

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapped

    def update(self, active):
        Switch.objects.filter(id=self.switch.id).update(active=active)

    def __enter__(self):
        self.switch, self.created = Switch.objects.get_or_create(name=self.name)
        self.was_active = bool(self.switch.active)
        if self.switch.active != self.active:
            self.update(self.active)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.created:
            self.switch.delete()
        else:
            self.update(self.was_active)
