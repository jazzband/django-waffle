from __future__ import annotations

import hashlib
from typing import Any

from django.conf import settings
from django.core.cache import BaseCache, caches

import waffle
from waffle import defaults


def get_setting(name: str, default: Any = None) -> Any:
    try:
        return getattr(settings, 'WAFFLE_' + name)
    except AttributeError:
        return getattr(defaults, name, default)


def keyfmt(k: str, v: str | None = None) -> str:
    prefix = get_setting('CACHE_PREFIX') + waffle.__version__
    if v is None:
        return prefix + k
    return prefix + hashlib.md5((k % v).encode('utf-8')).hexdigest()  # noqa: S324


def get_cache() -> BaseCache:
    CACHE_NAME = get_setting('CACHE_NAME')
    return caches[CACHE_NAME]
