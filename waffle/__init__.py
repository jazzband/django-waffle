from decimal import Decimal
import random
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed

from waffle.models import Flag, Sample, Switch


VERSION = (0, 9, 2)
__version__ = '.'.join(map(str, VERSION))


CACHE_PREFIX = getattr(settings, 'WAFFLE_CACHE_PREFIX', u'waffle:')
FLAG_CACHE_KEY = u'flag:%s'
FLAGS_ALL_CACHE_KEY = u'flags:all'
FLAG_USERS_CACHE_KEY = u'flag:%s:users'
FLAG_GROUPS_CACHE_KEY = u'flag:%s:groups'
SAMPLE_CACHE_KEY = u'sample:%s'
SAMPLES_ALL_CACHE_KEY = u'samples:all'
SWITCH_CACHE_KEY = u'switch:%s'
SWITCHES_ALL_CACHE_KEY = u'switches:all'
COOKIE_NAME = getattr(settings, 'WAFFLE_COOKIE', 'dwf_%s')
TEST_COOKIE_NAME = getattr(settings, 'WAFFLE_TESTING_COOKIE', 'dwft_%s')


def keyfmt(k, v=None):
    if v is None:
        return CACHE_PREFIX + k
    return CACHE_PREFIX + hashlib.md5(k % v).hexdigest()


class DoesNotExist(object):
    """The record does not exist."""
    @property
    def active(self):
        return getattr(settings, 'WAFFLE_SWITCH_DEFAULT', False)


def set_flag(request, flag_name, active=True, session_only=False):
    """Set a flag value on a request object."""
    if not hasattr(request, 'waffles'):
        request.waffles = {}
    request.waffles[flag_name] = [active, session_only]


def flag_is_active(request, flag_name):
    flag = cache.get(keyfmt(FLAG_CACHE_KEY, flag_name))
    if flag is None:
        if getattr(settings, 'WAFFLE_FLAG_AUTOCREATE', False):
            defaults = getattr(settings, 'WAFFLE_FLAG_DEFAULTS', {})
            flag, created = Flag.objects.get_or_create(name=flag_name,
                    defaults=defaults.get(flag_name, {}))
        else:
            try:
                flag = Flag.objects.get(name=flag_name)
            except Flag.DoesNotExist:
                return getattr(settings, 'WAFFLE_FLAG_DEFAULT', False)
        cache_flag(instance=flag)

    if getattr(settings, 'WAFFLE_OVERRIDE', False):
        if flag_name in request.GET:
            return request.GET[flag_name] == '1'

    if flag.everyone:
        return True
    elif flag.everyone is False:
        return False

    if flag.testing:  # Testing mode is on.
        tc = TEST_COOKIE_NAME % flag_name
        if tc in request.GET:
            on = request.GET[tc] == '1'
            if not hasattr(request, 'waffle_tests'):
                request.waffle_tests = {}
            request.waffle_tests[flag_name] = on
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

    flag_users = cache.get(keyfmt(FLAG_USERS_CACHE_KEY, flag.name))
    if flag_users is None:
        flag_users = flag.users.all()
        cache_flag(instance=flag)
    if user in flag_users:
        return True

    flag_groups = cache.get(keyfmt(FLAG_GROUPS_CACHE_KEY, flag.name))
    if flag_groups is None:
        flag_groups = flag.groups.all()
        cache_flag(instance=flag)
    user_groups = user.groups.all()
    for group in flag_groups:
        if group in user_groups:
            return True

    if flag.percent > 0:
        if not hasattr(request, 'waffles'):
            request.waffles = {}
        elif flag_name in request.waffles:
            return request.waffles[flag_name][0]

        cookie = COOKIE_NAME % flag_name
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
    switch = cache.get(keyfmt(SWITCH_CACHE_KEY, switch_name))
    if switch is None:
        if getattr(settings, 'WAFFLE_SWITCH_AUTOCREATE', False):
            defaults = getattr(settings, 'WAFFLE_SWITCH_DEFAULTS', {})
            switch, created = Switch.objects.get_or_create(name=switch_name,
                    defaults=defaults.get(switch_name, {}))
        else:
            try:
                switch = Switch.objects.get(name=switch_name)
            except Switch.DoesNotExist:
                switch = DoesNotExist()
                switch.name = switch_name
            cache_switch(instance=switch)
    return switch.active


def sample_is_active(sample_name):
    sample = cache.get(keyfmt(SAMPLE_CACHE_KEY, sample_name))
    if sample is None:
        if getattr(settings, 'WAFFLE_SAMPLE_AUTOCREATE', False):
            defaults = getattr(settings, 'WAFFLE_SAMPLE_DEFAULTS', {})
            sample, created = Sample.objects.get_or_create(name=sample_name,
                    defaults=defaults.get(sample_name, {}))
        else:
            try:
                sample = Sample.objects.get(name=sample_name)
            except Sample.DoesNotExist:
                return getattr(settings, 'WAFFLE_SAMPLE_DEFAULT', False)
        cache_sample(instance=sample)

    return Decimal(str(random.uniform(0, 100))) <= sample.percent


def cache_flag(**kwargs):
    action = kwargs.get('action', None)
    # action is included for m2m_changed signal. Only cache on the post_*.
    if not action or action in ['post_add', 'post_remove', 'post_clear']:
        f = kwargs.get('instance')
        cache.add(keyfmt(FLAG_CACHE_KEY, f.name), f)
        cache.add(keyfmt(FLAG_USERS_CACHE_KEY, f.name), f.users.all())
        cache.add(keyfmt(FLAG_GROUPS_CACHE_KEY, f.name), f.groups.all())


def uncache_flag(**kwargs):
    flag = kwargs.get('instance')
    data = {
        keyfmt(FLAG_CACHE_KEY, flag.name): None,
        keyfmt(FLAG_USERS_CACHE_KEY, flag.name): None,
        keyfmt(FLAG_GROUPS_CACHE_KEY, flag.name): None,
        keyfmt(FLAGS_ALL_CACHE_KEY): None
    }
    cache.set_many(data, 5)

post_save.connect(uncache_flag, sender=Flag, dispatch_uid='save_flag')
post_delete.connect(uncache_flag, sender=Flag, dispatch_uid='delete_flag')
m2m_changed.connect(uncache_flag, sender=Flag.users.through,
                    dispatch_uid='m2m_flag_users')
m2m_changed.connect(uncache_flag, sender=Flag.groups.through,
                    dispatch_uid='m2m_flag_groups')


def cache_sample(**kwargs):
    sample = kwargs.get('instance')
    cache.add(keyfmt(SAMPLE_CACHE_KEY, sample.name), sample)


def uncache_sample(**kwargs):
    sample = kwargs.get('instance')
    cache.set(keyfmt(SAMPLE_CACHE_KEY, sample.name), None, 5)
    cache.set(keyfmt(SAMPLES_ALL_CACHE_KEY), None, 5)

post_save.connect(uncache_sample, sender=Sample, dispatch_uid='save_sample')
post_delete.connect(uncache_sample, sender=Sample,
                    dispatch_uid='delete_sample')


def cache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.add(keyfmt(SWITCH_CACHE_KEY, switch.name), switch)


def uncache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.set(keyfmt(SWITCH_CACHE_KEY, switch.name), None, 5)
    cache.set(keyfmt(SWITCHES_ALL_CACHE_KEY), None, 5)

post_delete.connect(uncache_switch, sender=Switch,
                    dispatch_uid='delete_switch')
post_save.connect(uncache_switch, sender=Switch, dispatch_uid='save_switch')
