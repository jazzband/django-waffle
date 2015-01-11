from __future__ import unicode_literals, absolute_import

import hashlib

from django.conf import settings

from . import defaults


def get_setting(name):
    try:
        return getattr(settings, 'WAFFLE_' + name)
    except AttributeError:
        return getattr(defaults, name)


def keyfmt(k, v=None):
    prefix = get_setting('CACHE_PREFIX')
    if v is None:
        key = prefix + k
    else:
        key = prefix + hashlib.md5((k % v).encode('utf-8')).hexdigest()
    return key.encode('utf-8')
