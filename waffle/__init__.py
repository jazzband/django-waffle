from decimal import Decimal
import random

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed

from waffle.models import Flag, Switch


FLAG_CACHE_KEY = u'waffle:flag:{n}'
FLAG_USERS_CACHE_KEY = u'waffle:flag:{n}:users'
FLAG_GROUPS_CACHE_KEY = u'waffle:flag:{n}:groups'
SWITCH_CACHE_KEY = u'waffle:switch:{n}'


def flag_is_active(request, flag_name):
    flag = cache.get(FLAG_CACHE_KEY.format(n=flag_name))
    if not flag:
        try:
            flag = Flag.objects.get(name=flag_name)
            cache_flag(instance=flag)
        except Flag.DoesNotExist:
            return getattr(settings, 'WAFFLE_DEFAULT', False)

    if getattr(settings, 'WAFFLE_OVERRIDE', False):
        if flag_name in request.GET:
            return request.GET[flag_name] == '1'

    if flag.everyone:
        return True
    elif flag.everyone == False:
        return False

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
        request.waffles[flag_name] = [False, flag.rollout]

        format = getattr(settings, 'WAFFLE_COOKIE', 'dwf_%s')
        cookie = format % flag_name
        if cookie in request.COOKIES:
            request.waffles[flag_name][0] = (request.COOKIES[cookie] == 'True')
            return request.waffles[flag_name][0]

        rand = Decimal(random.randint(0, 999)) / 10
        if rand <= flag.percent:
            request.waffles[flag_name][0] = True
            return True

    return False


def switch_is_active(switch_name):
    switch = cache.get(SWITCH_CACHE_KEY.format(n=switch_name))
    if not switch:
        try:
            switch = Switch.objects.get(name=switch_name)
            cache_switch(instance=switch)
        except Switch.DoesNotExist:
            return False

    return switch.active


def cache_flag(**kwargs):
    action = kwargs.get('action', None)
    # action is included for m2m_changed signal. Only cache on the post_*.
    if not action or action in ['post_add', 'post_remove', 'post_clear']:
        f = kwargs.get('instance')
        cache.set(FLAG_CACHE_KEY.format(n=f.name), f)
        cache.set(FLAG_USERS_CACHE_KEY.format(n=f.name), f.users.all())
        cache.set(FLAG_GROUPS_CACHE_KEY.format(n=f.name), f.groups.all())

post_save.connect(cache_flag, sender=Flag, dispatch_uid='cache_flag')
m2m_changed.connect(cache_flag, sender=Flag.users.through,
                    dispatch_uid='cache_flag_users')
m2m_changed.connect(cache_flag, sender=Flag.groups.through,
                    dispatch_uid='cache_flag_groups')


def uncache_flag(**kwargs):
    flag = kwargs.get('instance')
    cache.delete_many([FLAG_CACHE_KEY.format(n=flag.name),
                       FLAG_USERS_CACHE_KEY.format(n=flag.name),
                       FLAG_GROUPS_CACHE_KEY.format(n=flag.name)])

post_delete.connect(uncache_flag, sender=Flag, dispatch_uid='uncache_flag')


def cache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.set(SWITCH_CACHE_KEY.format(n=switch.name), switch)

post_save.connect(cache_switch, sender=Switch, dispatch_uid='cache_switch')


def ucache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.delete(SWITCH_CACHE_KEY.format(n=switch.name))

post_delete.connect(ucache_switch, sender=Switch,
                    dispatch_uid='uncache_switch')
