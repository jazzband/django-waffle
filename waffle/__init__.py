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


def flag_is_active(request, flag_name, session_key="feature"):
    from .models import cache_flag, Flag
    from .compat import cache

    if hasattr(request, 'session'):
        try:
            flag = Flag.objects.get(name=flag_name)
            if request.session.get(session_key) == flag.name:
                return True
        except Flag.DoesNotExist:
            pass

    flag = cache.get(keyfmt(settings.FLAG_CACHE_KEY, flag_name))
    if flag is None:
        try:
            flag = Flag.objects.get(name=flag_name)
            cache_flag(instance=flag)
        except Flag.DoesNotExist:
            return settings.FLAG_DEFAULT

    if settings.OVERRIDE:
        if flag_name in request.GET:
            return request.GET[flag_name] == '1'

    if flag.everyone:
        return True
    elif flag.everyone is False:
        return False

    if flag.testing:  # Testing mode is on.
        tc = settings.TEST_COOKIE_NAME % flag_name
        if tc in request.GET:
            on = request.GET[tc] == '1'
            if not hasattr(request, 'waffle_tests'):
                request.waffle_tests = {}
            request.waffle_tests[flag_name] = on
            return on
        if tc in request.COOKIES:
            return request.COOKIES[tc] == 'True'

    if hasattr(request, 'user'):
        user = request.user

        if flag.authenticated and user.is_authenticated():
            return True

        if flag.staff and user.is_staff:
            return True

        if flag.superusers and user.is_superuser:
            return True

        flag_users = cache.get(keyfmt(settings.FLAG_USERS_CACHE_KEY, flag.name))
        if flag_users is None:
            flag_users = flag.users.all()
            cache_flag(instance=flag)
        if user in flag_users:
            return True

        flag_groups = cache.get(keyfmt(settings.FLAG_GROUPS_CACHE_KEY, flag.name))
        if flag_groups is None:
            flag_groups = flag.groups.all()
            cache_flag(instance=flag)
        user_groups = user.groups.all()
        for group in flag_groups:
            if group in user_groups:
                return True

    if flag.languages:
        languages = flag.languages.split(',')
        if (hasattr(request, 'LANGUAGE_CODE') and
                request.LANGUAGE_CODE in languages):
            return True

    if flag.percent and flag.percent > 0:
        if not hasattr(request, 'waffles'):
            request.waffles = {}
        elif flag_name in request.waffles:
            return request.waffles[flag_name][0]

        cookie = settings.COOKIE_NAME % flag_name
        if cookie in request.COOKIES:
            flag_active = (request.COOKIES[cookie] == 'True')
            set_flag(request, flag_name, flag_active, flag.rollout)
            return flag_active

        if Decimal(str(random.uniform(0, 100))) <= flag.percent:
            set_flag(request, flag_name, True, flag.rollout)
            return True
        set_flag(request, flag_name, False, flag.rollout)

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
