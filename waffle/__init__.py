from collections import defaultdict
from decimal import Decimal
import random
import hashlib


from . import settings


VERSION = (0, 10, 1)
__version__ = '.'.join(map(str, VERSION))


def keyfmt(k, v=None):
    if v is None:
        return settings.CACHE_PREFIX + k
    return settings.CACHE_PREFIX + hashlib.md5((k % v).encode('utf-8')).hexdigest()


class DoesNotExist(object):
    """The record does not exist."""
    @property
    def active(self):
        return settings.SWITCH_DEFAULT


def set_flag(request, flag_name, active=True, session_only=False):
    """Set a flag value on a request object."""
    if not hasattr(request, 'waffles'):
        request.waffles = {}
    request.waffles[flag_name] = [active, session_only]


def get_flags(flag_names):
    from .compat import cache
    from .models import Flag, cache_flags

    flag_keys = [keyfmt(settings.FLAG_CACHE_KEY, f) for f in flag_names]
    cached_flags = cache.get_many(flag_keys).values()
    cached_flag_names = set([f.name for f in cached_flags])
    missing_flag_names = set(flag_names).difference(cached_flag_names)
    uncached_flags = Flag.objects.filter(name__in=missing_flag_names)
    cache_flags(instances=uncached_flags)
    uncached_flag_names = set([f.name for f in uncached_flags])
    missing_flag_names = missing_flag_names.difference(uncached_flag_names)
    missing_flags = [Flag(name=f_name, everyone=settings.FLAG_DEFAULT) for f_name in missing_flag_names]

    return list(cached_flags) + list(uncached_flags), missing_flags


def flags_are_active(request, flag_names):
    from .compat import cache

    full_flags, missing_flags = get_flags(flag_names)

    flag_user_keys = [keyfmt(settings.FLAG_USERS_CACHE_KEY, f.name) for f in full_flags]
    flag_users = defaultdict(list, cache.get_many(flag_user_keys))
    flag_group_keys = [keyfmt(settings.FLAG_GROUPS_CACHE_KEY, f.name) for f in full_flags]
    flag_groups = defaultdict(list, cache.get_many(flag_group_keys))

    try:
        user_groups = request.user.groups.all()
    except ValueError:
        user_groups = None

    flags = [(f, _full_flag_is_active(request, f, flag_users[keyfmt(settings.FLAG_USERS_CACHE_KEY, f.name)], flag_groups[keyfmt(settings.FLAG_GROUPS_CACHE_KEY, f.name)], user_groups)) for f in full_flags + missing_flags]
    return flags


def flag_is_active(request, flag_name):
    flag_names = [flag_name, ]
    flags = flags_are_active(request, flag_names)
    return flags[0][1]


def _full_flag_is_active(request, flag, flag_users, flag_groups, user_groups):
    if settings.OVERRIDE:
        if flag.name in request.GET:
            return request.GET[flag.name] == '1'

    if flag.everyone:
        return True
    elif flag.everyone is False:
        return False

    if flag.testing:  # Testing mode is on.
        tc = settings.TEST_COOKIE_NAME % flag.name
        if tc in request.GET:
            on = request.GET[tc] == '1'
            if not hasattr(request, 'waffle_tests'):
                request.waffle_tests = {}
            request.waffle_tests[flag.name] = on
            return on
        if tc in request.COOKIES:
            return request.COOKIES[tc] == 'True'

    user = request.user

    if flag.authenticated and user.is_authenticated():
        return True

    if flag.staff and user.is_staff:
        return True

    if flag.superusers and user.is_superuser:
        return True

    if flag.languages:
        languages = flag.languages.split(',')
        if (hasattr(request, 'LANGUAGE_CODE') and
                request.LANGUAGE_CODE in languages):
            return True

    if user in flag_users:
        return True

    for group in flag_groups:
        if group in user_groups:
            return True

    if flag.percent and flag.percent > 0:
        if not hasattr(request, 'waffles'):
            request.waffles = {}
        elif flag.name in request.waffles:
            return request.waffles[flag.name][0]

        cookie = settings.COOKIE_NAME % flag.name
        if cookie in request.COOKIES:
            flag_active = (request.COOKIES[cookie] == 'True')
            set_flag(request, flag.name, flag_active, flag.rollout)
            return flag_active

        if Decimal(str(random.uniform(0, 100))) <= flag.percent:
            set_flag(request, flag.name, True, flag.rollout)
            return True
        set_flag(request, flag.name, False, flag.rollout)

    return False


def switch_is_active(switch_name):
    from .models import cache_switch, Switch
    from .compat import cache

    switch = cache.get(keyfmt(settings.SWITCH_CACHE_KEY, switch_name))
    if switch is None:
        try:
            switch = Switch.objects.get(name=switch_name)
            cache_switch(instance=switch)
        except Switch.DoesNotExist:
            switch = DoesNotExist()
            switch.name = switch_name
            cache_switch(instance=switch)
    return switch.active


def sample_is_active(sample_name):
    from .models import cache_sample, Sample
    from .compat import cache

    sample = cache.get(keyfmt(settings.SAMPLE_CACHE_KEY, sample_name))
    if sample is None:
        try:
            sample = Sample.objects.get(name=sample_name)
            cache_sample(instance=sample)
        except Sample.DoesNotExist:
            return settings.SAMPLE_DEFAULT

    return Decimal(str(random.uniform(0, 100))) <= sample.percent
