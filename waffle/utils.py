from __future__ import unicode_literals, absolute_import

import hashlib
import warnings

from django.apps import apps
from django.conf import settings
from django.core.cache import caches

import waffle
from waffle import defaults


def get_setting(name):
    try:
        waffle_settings = getattr(settings, 'WAFFLE')
        return waffle_settings[name]
    except (AttributeError, KeyError):
        try:
            setting = getattr(settings, 'WAFFLE_' + name)
            warnings.warn(
                'WAFFLE_[setting] is deprecated. '
                'Use the WAFFLE dictionary instead',
                DeprecationWarning)
            return setting
        except AttributeError:
            return getattr(defaults, name)


def keyfmt(k, v=None):
    prefix = get_setting('CACHE_PREFIX') + waffle.__version__
    if v is None:
        key = prefix + k
    else:
        key = prefix + hashlib.md5((k % v).encode('utf-8')).hexdigest()
    return key.encode('utf-8')


def get_cache():
    CACHE_NAME = get_setting('CACHE_NAME')
    return caches[CACHE_NAME]


def get_flag_model():
    model_name = get_setting('FLAG_CLASS')
    app_name = model_name.split('.')[0]
    model_name = model_name.split('.')[-1]
    config = apps.get_app_config(app_name)
    return config.get_model(model_name)
