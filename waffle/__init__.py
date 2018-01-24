from __future__ import unicode_literals

from waffle.utils import get_cache, get_setting, keyfmt

VERSION = (0, 13, 0)
__version__ = '.'.join(map(str, VERSION))


def flag_is_active(request, flag_name):
    from .models import Flag

    flag = Flag.get(flag_name)
    return flag.is_active(request)


def switch_is_active(switch_name):
    from .models import Switch

    switch = Switch.get(switch_name)
    return switch.is_active()


def sample_is_active(sample_name):
    from .models import Sample

    sample = Sample.get(sample_name)
    return sample.is_active()
