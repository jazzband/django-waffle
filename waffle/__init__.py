from __future__ import unicode_literals

from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

from waffle.utils import get_cache, get_flag_model, get_setting, keyfmt

VERSION = (0, 15, 2)
__version__ = '.'.join(map(str, VERSION))
default_app_config = 'waffle.apps.WaffleConfig'


def flag_is_active(request, flag_name):
    flag = get_flag_model().get(flag_name)
    return flag.is_active(request)


def switch_is_active(switch_name):
    from .models import Switch

    switch = Switch.get(switch_name)
    return switch.is_active()


def sample_is_active(sample_name):
    from .models import Sample

    sample = Sample.get(sample_name)
    return sample.is_active()
