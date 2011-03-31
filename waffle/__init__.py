from decimal import Decimal
import random

from django.conf import settings
from django.core.cache import cache

from waffle.models import Flag, Switch


def flag_is_active(request, flag_name):
    key = 'waffle:flag:{n}'.format(n=flag_name)
    flag = cache.get(key)
    if not flag:
        try:
            flag = Flag.objects.get(name=flag_name)
            cache.set(key, flag)
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

    if user in flag.users.all():
        return True

    for group in flag.groups.all():
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
    key = 'waffle:switch:{n}'.format(n=switch_name)
    switch = cache.get(key)
    if not switch:
        try:
            switch = Switch.objects.get(name=switch_name)
            cache.set(key, switch)
        except Switch.DoesNotExist:
            return False

    return switch.active
