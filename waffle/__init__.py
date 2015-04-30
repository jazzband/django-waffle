from decimal import Decimal
import random

from waffle.utils import get_setting, keyfmt
from django.contrib.sites.models import Site


VERSION = (0, 10, 1)
__version__ = '.'.join(map(str, VERSION))


def set_flag(request, flag_name, active=True, session_only=False):
    """Set a flag value on a request object."""
    if not hasattr(request, 'waffles'):
        request.waffles = {}
    request.waffles[flag_name] = [active, session_only]


def flag_is_active(request, flag_name):
    from .models import cache_flag, Flag
    from .compat import cache

    current_site = Site.objects.get_current()
    flag = cache.get(keyfmt(get_setting('FLAG_CACHE_KEY'), flag_name, current_site))
    if flag is None:
        try:
            flag = Flag.objects.get(name=flag_name, site=current_site)
            cache_flag(instance=flag)
        except Flag.DoesNotExist:
            try:
                flag = Flag.objects.get(name=flag_name, site__isnull=True)
                cache_flag(instance=flag)
            except Flag.DoesNotExist:
                return get_setting('FLAG_DEFAULT')

    if get_setting('OVERRIDE'):
        if flag_name in request.GET:
            return request.GET[flag_name] == '1'

    if flag.everyone:
        return True
    elif flag.everyone is False:
        return False

    if flag.testing:  # Testing mode is on.
        tc = get_setting('TEST_COOKIE') % flag_name
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

    flag_users = cache.get(keyfmt(get_setting('FLAG_USERS_CACHE_KEY'),
                                              flag.name, current_site))
    if flag_users is None:
        flag_users = flag.users.all()
        cache_flag(instance=flag)
    if user in flag_users:
        return True

    flag_groups = cache.get(keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'),
                                   flag.name, current_site))
    if flag_groups is None:
        flag_groups = flag.groups.all()
        cache_flag(instance=flag)
    user_groups = user.groups.all()
    for group in flag_groups:
        if group in user_groups:
            return True

    if flag.percent and flag.percent > 0:
        if not hasattr(request, 'waffles'):
            request.waffles = {}
        elif flag_name in request.waffles:
            return request.waffles[flag_name][0]

        cookie = get_setting('COOKIE') % flag_name
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

    current_site = Site.objects.get_current()
    switch = cache.get(keyfmt(get_setting('SWITCH_CACHE_KEY'), switch_name, current_site))
    if switch is None:
        try:
            switch = Switch.objects.get(name=switch_name, site=current_site)
            cache_switch(instance=switch)
        except Switch.DoesNotExist:
            try:
                switch = Switch.objects.get(name=switch_name, site__isnull=True)
                cache_switch(instance=switch)
            except Switch.DoesNotExist:
                return get_setting('SWITCH_DEFAULT')
    return switch.active


def sample_is_active(sample_name):
    from .models import cache_sample, Sample
    from .compat import cache

    current_site = Site.objects.get_current()
    sample = cache.get(keyfmt(get_setting('SAMPLE_CACHE_KEY'), sample_name, current_site))
    if sample is None:
        try:
            sample = Sample.objects.get(name=sample_name, site=current_site)
            cache_sample(instance=sample)
        except Sample.DoesNotExist:
            try:
                sample = Sample.objects.get(name=sample_name, site__isnull=True)
                cache_sample(instance=sample)
            except Sample.DoesNotExist:
                return get_setting('SAMPLE_DEFAULT')

    return Decimal(str(random.uniform(0, 100))) <= sample.percent
