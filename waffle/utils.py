from __future__ import unicode_literals, absolute_import

import hashlib

from django.conf import settings

from . import defaults


def get_setting(name):
    try:
        return getattr(settings, 'WAFFLE_' + name)
    except AttributeError:
        return getattr(defaults, name)


def keyfmt(k, v=None, s=None):
    """ create a unique cache key
        k = {}_CACHE_KEY see defaults.py
        v = switch/flag/sample name
        s = site
    """
    prefix = get_setting('CACHE_PREFIX')
    if v is None:
        key = prefix + k
    else:
        if s is None:
            site_unique = v
        else:
            site_unique = '%s:%d' % (v, s.id)
        key = prefix + hashlib.md5((k % site_unique).encode('utf-8')).hexdigest()
    return key.encode('utf-8')
