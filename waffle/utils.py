import hashlib

from . import settings


def keyfmt(k, v=None):
    if v is None:
        return settings.CACHE_PREFIX + k
    return settings.CACHE_PREFIX + hashlib.md5(k % v).hexdigest()
