from __future__ import unicode_literals

from decimal import Decimal
import random

from waffle.utils import get_setting, keyfmt, get_cache


VERSION = (0, 11, 1)
__version__ = '.'.join(map(str, VERSION))


class DoesNotExist(object):
    """The record does not exist."""
    @property
    def active(self):
        return get_setting('SWITCH_DEFAULT')


def flag_is_active(request, flag_name):
    from .models import Flag

    flag = Flag.get(flag_name)
    return flag.is_active(request)


def switch_is_active(switch_name):
    from .models import Switch

    switch = Switch.get(switch_name)
    return switch.is_active()


def sample_is_active(sample_name):
    from .models import cache_sample, Sample
    cache = get_cache()

    sample = cache.get(keyfmt(get_setting('SAMPLE_CACHE_KEY'), sample_name))
    if sample is None:
        try:
            sample = Sample.objects.get(name=sample_name)
            cache_sample(instance=sample)
        except Sample.DoesNotExist:
            return get_setting('SAMPLE_DEFAULT')

    return Decimal(str(random.uniform(0, 100))) <= sample.percent
