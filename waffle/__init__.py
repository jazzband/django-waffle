from decimal import Decimal
import random

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed

from waffle.models import Flag, Sample, Switch


VERSION = (0, 8, 0)
__version__ = '.'.join(map(str, VERSION))


CACHE_PREFIX = getattr(settings, 'WAFFLE_CACHE_PREFIX', u'waffle:')
FLAG_CACHE_KEY = CACHE_PREFIX + u'flag:{n}'
FLAGS_ALL_CACHE_KEY = CACHE_PREFIX + u'flags:all'
FLAG_USERS_CACHE_KEY = CACHE_PREFIX + u'flag:{n}:users'
FLAG_GROUPS_CACHE_KEY = CACHE_PREFIX + u'flag:{n}:groups'
SAMPLE_CACHE_KEY = CACHE_PREFIX + u'sample:{n}'
SAMPLES_ALL_CACHE_KEY = CACHE_PREFIX + u'samples:all'
SWITCH_CACHE_KEY = CACHE_PREFIX + u'switch:{n}'
SWITCHES_ALL_CACHE_KEY = CACHE_PREFIX + u'switches:all'
COOKIE_NAME = getattr(settings, 'WAFFLE_COOKIE', 'dwf_%s')
TEST_COOKIE_NAME = getattr(settings, 'WAFFLE_TESTING_COOKIE', 'dwft_%s')


def flag_is_active(request, flag_name):
    flag = cache.get(FLAG_CACHE_KEY.format(n=flag_name))
    if flag is None:
        try:
            flag = Flag.objects.get(name=flag_name)
            cache_flag(instance=flag)
        except Flag.DoesNotExist:
            return getattr(settings, 'WAFFLE_FLAG_DEFAULT', False)

    if getattr(settings, 'WAFFLE_OVERRIDE', False):
        if flag_name in request.GET:
            return request.GET[flag_name] == '1'


    if flag.everyone:
        return True
    elif flag.everyone == False:
        return False

    if flag.testing:  # Testing mode is on.
        tc = TEST_COOKIE_NAME % flag_name
        if tc in request.COOKIES:
            return request.COOKIES[tc] == 'True'
        if tc in request.GET:
            on = request.GET[tc] == '1'
            if not hasattr(request, 'waffle_tests'):
                request.waffle_tests = {}
            request.waffle_tests[flag_name] = on
            return on

    user = request.user

    if flag.authenticated and user.is_authenticated():
        return True

    if flag.staff and user.is_staff:
        return True

    if flag.superusers and user.is_superuser:
        return True

    flag_users = cache.get(FLAG_USERS_CACHE_KEY.format(n=flag.name))
    if flag_users == None:
        flag_users = flag.users.all()
        cache_flag(instance=flag)
    if user in flag_users:
        return True

    flag_groups = cache.get(FLAG_GROUPS_CACHE_KEY.format(n=flag.name))
    if flag_groups == None:
        flag_groups = flag.groups.all()
        cache_flag(instance=flag)
    for group in flag_groups:
        if group in user.groups.all():
            return True

    if flag.percent > 0:
        if not hasattr(request, 'waffles'):
            request.waffles = {}
        elif flag_name in request.waffles:
            return request.waffles[flag_name][0]
        request.waffles[flag_name] = [False, flag.rollout]

        cookie = COOKIE_NAME % flag_name
        if cookie in request.COOKIES:
            request.waffles[flag_name][0] = (request.COOKIES[cookie] == 'True')
            return request.waffles[flag_name][0]

        if Decimal(str(random.uniform(0, 100))) <= flag.percent:
            request.waffles[flag_name][0] = True
            return True

    return False


def switch_is_active(switch_name):
    switch = cache.get(SWITCH_CACHE_KEY.format(n=switch_name))
    if switch is None:
        try:
            switch = Switch.objects.get(name=switch_name)
            cache_switch(instance=switch)
        except Switch.DoesNotExist:
            return getattr(settings, 'WAFFLE_SWITCH_DEFAULT', False)

    return switch.active


def sample_is_active(sample_name):
    sample = cache.get(SAMPLE_CACHE_KEY.format(n=sample_name))
    if sample is None:
        try:
            sample = Sample.objects.get(name=sample_name)
            cache_sample(instance=sample)
        except Sample.DoesNotExist:
            return getattr(settings, 'WAFFLE_SAMPLE_DEFAULT', False)

    return Decimal(str(random.uniform(0, 100))) <= sample.percent


def cache_flag(**kwargs):
    action = kwargs.get('action', None)
    # action is included for m2m_changed signal. Only cache on the post_*.
    if not action or action in ['post_add', 'post_remove', 'post_clear']:
        f = kwargs.get('instance')
        cache.add(FLAG_CACHE_KEY.format(n=f.name), f)
        cache.add(FLAG_USERS_CACHE_KEY.format(n=f.name), f.users.all())
        cache.add(FLAG_GROUPS_CACHE_KEY.format(n=f.name), f.groups.all())


def uncache_flag(**kwargs):
    flag = kwargs.get('instance')
    data = {
        FLAG_CACHE_KEY.format(n=flag.name): None,
        FLAG_USERS_CACHE_KEY.format(n=flag.name): None,
        FLAG_GROUPS_CACHE_KEY.format(n=flag.name): None,
        FLAGS_ALL_CACHE_KEY: None
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
    cache.add(SAMPLE_CACHE_KEY.format(n=sample.name), sample)


def uncache_sample(**kwargs):
    sample = kwargs.get('instance')
    cache.set(SAMPLE_CACHE_KEY.format(n=sample.name), None, 5)
    cache.set(SAMPLES_ALL_CACHE_KEY, None, 5)

post_save.connect(uncache_sample, sender=Sample, dispatch_uid='save_sample')
post_delete.connect(uncache_sample, sender=Sample,
                    dispatch_uid='delete_sample')


def cache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.add(SWITCH_CACHE_KEY.format(n=switch.name), switch)


def uncache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.set(SWITCH_CACHE_KEY.format(n=switch.name), None, 5)
    cache.set(SWITCHES_ALL_CACHE_KEY, None, 5)

post_delete.connect(uncache_switch, sender=Switch,
                    dispatch_uid='delete_switch')
post_save.connect(uncache_switch, sender=Switch, dispatch_uid='save_switch')
