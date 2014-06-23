import hashlib

from django.utils.encoding import smart_bytes

from . import settings


def keyfmt(k, v=None):
    if v is None:
        return settings.CACHE_PREFIX + k

    value = smart_bytes(k % v)

    return settings.CACHE_PREFIX + hashlib.md5(value).hexdigest()
