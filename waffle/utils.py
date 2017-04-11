from __future__ import unicode_literals, absolute_import

import hashlib

from django.conf import settings
from django.core.cache import caches

import waffle
from waffle import defaults


def get_setting(name, more_defaults=None):
    """
    :param name: Name of WAFFLE_* setting (value of *) to get from settings or waffle.defaults
    :param more_defaults: additional app-defined defaults
    :return: the setting value
    """
    try:
        return getattr(settings, 'WAFFLE_' + name)
    except AttributeError:
        try:
            return getattr(defaults, name)
        except AttributeError:
            more_defaults = more_defaults or {}
            return more_defaults[name]


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
