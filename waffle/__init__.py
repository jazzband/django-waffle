from __future__ import unicode_literals

import random
from decimal import Decimal

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from waffle.utils import get_setting, keyfmt, get_cache


VERSION = (0, 12, 0, 'a', 1)
__version__ = '.'.join(map(str, VERSION))


def flag_is_active(request, flag_name):
    flag = get_waffle_flag_model().get(flag_name)
    return flag.is_active(request)


def switch_is_active(switch_name):
    from .models import Switch

    switch = Switch.get(switch_name)
    return switch.is_active()


def sample_is_active(sample_name):
    from .models import Sample

    sample = Sample.get(sample_name)
    return sample.is_active()


def get_waffle_flag_model():
    """
    Returns the waffle Flag model that is active in this project.
    """
    # Assume default WAFFLE_FLAG_MODEL.
    # At some point it would be helpful to require this to be defined explicitly, but not for now
    # This remove pain from upgrading.
    flag_model = getattr(settings, 'WAFFLE_FLAG_MODEL', 'waffle.Flag')

    try:
        return django_apps.get_model(flag_model)
    except ValueError:
        raise ImproperlyConfigured("WAFFLE_FLAG_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "WAFFLE_FLAG_MODEL refers to model '{}' that has not been installed".format(
                settings.WAFFLE_FLAG_MODEL
            )
        )
