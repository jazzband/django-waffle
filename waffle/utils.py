from __future__ import unicode_literals, absolute_import

import hashlib

import django
from django.conf import settings
from django.core.cache import caches

import waffle
from waffle import defaults


def get_setting(name):
    try:
        return getattr(settings, 'WAFFLE_' + name)
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


if django.VERSION >= (1, 10):
    def is_authenticated(user):
        return user.is_authenticated
else:
    def is_authenticated(user):
        return user.is_authenticated()
