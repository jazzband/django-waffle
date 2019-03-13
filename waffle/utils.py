from __future__ import unicode_literals, absolute_import

import hashlib
import ipaddress

from django.conf import settings
from django.core.cache import caches
from ipware import get_client_ip

import waffle
from waffle import defaults


def get_setting(name, default=None):
    try:
        return getattr(settings, 'WAFFLE_' + name)
    except AttributeError:
        return getattr(defaults, name, default)


def keyfmt(k, v=None):
    prefix = get_setting('CACHE_PREFIX') + waffle.__version__
    if v is None:
        key = prefix + k
    else:
        key = prefix + hashlib.md5((k % v).encode('utf-8')).hexdigest()
    return key


def get_cache():
    CACHE_NAME = get_setting('CACHE_NAME')
    return caches[CACHE_NAME]


def ip_in_cidr_range(ip, range):
    network = ipaddress.ip_network(range)
    return ipaddress.ip_address(ip) in network


def request_in_cidr_range(request, range):
    ip, is_routable = get_client_ip(request)

    return ip_in_cidr_range(ip, range)
