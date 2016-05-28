from __future__ import unicode_literals

from decimal import Decimal
import random

try:
    from django.utils import timezone as datetime
except ImportError:
    from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.utils.encoding import python_2_unicode_compatible

from waffle.utils import get_setting, keyfmt, get_cache


cache = get_cache()
CACHE_EMPTY = '-'


def set_flag(request, flag_name, active=True, session_only=False):
    """Set a flag value on a request object."""
    if not hasattr(request, 'waffles'):
        request.waffles = {}
    request.waffles[flag_name] = [active, session_only]


@python_2_unicode_compatible
class Flag(models.Model):
    """A feature flag.

    Flags are active (or not) on a per-request basis.

    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    everyone = models.NullBooleanField(blank=True, help_text=(
        'Flip this flag on (Yes) or off (No) for everyone, overriding all '
        'other settings. Leave as Unknown to use normally.'))
    percent = models.DecimalField(max_digits=3, decimal_places=1, null=True,
                                  blank=True, help_text=(
        'A number between 0.0 and 99.9 to indicate a percentage of users for '
        'whom this flag will be active.'))
    testing = models.BooleanField(default=False, help_text=(
        'Allow this flag to be set for a session for user testing.'))
    superusers = models.BooleanField(default=True, help_text=(
        'Flag always active for superusers?'))
    staff = models.BooleanField(default=False, help_text=(
        'Flag always active for staff?'))
    authenticated = models.BooleanField(default=False, help_text=(
        'Flag always active for authenticate users?'))
    languages = models.TextField(blank=True, default='', help_text=(
        'Activate this flag for users with one of these languages (comma '
        'separated list)'))
    groups = models.ManyToManyField(Group, blank=True, help_text=(
        'Activate this flag for these user groups.'))
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
        help_text=('Activate this flag for these users.'))
    rollout = models.BooleanField(default=False, help_text=(
        'Activate roll-out mode?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Flag is used.'))
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Flag was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Flag was last modified.'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Flag, self).save(*args, **kwargs)

    @classmethod
    def _cache_key(cls, name):
        return keyfmt(get_setting('FLAG_CACHE_KEY'), name)

    @classmethod
    def get(cls, name):
        cache_key = cls._cache_key(name)
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return cls()
        if cached:
            return cached

        try:
            flag = cls.objects.get(name=name)
        except cls.DoesNotExist:
            cache.add(cache_key, CACHE_EMPTY)
            return cls()

        # TODO: Populate many-to-many fields somehow
        cache.add(cache_key, flag)
        return flag

    def is_active(self, request):
        # Return default for fake flags.
        if not self.pk:
            return get_setting('FLAG_DEFAULT')

        if get_setting('OVERRIDE'):
            if self.name in request.GET:
                return request.GET[self.name] == '1'

        if self.everyone:
            return True
        elif self.everyone is False:
            return False

        if self.testing:  # Testing mode is on.
            tc = get_setting('TEST_COOKIE') % self.name
            if tc in request.GET:
                on = request.GET[tc] == '1'
                if not hasattr(request, 'waffle_tests'):
                    request.waffle_tests = {}
                request.waffle_tests[self.name] = on
                return on
            if tc in request.COOKIES:
                return request.COOKIES[tc] == 'True'

        user = request.user

        if self.authenticated and user.is_authenticated():
            return True

        if self.staff and getattr(user, 'is_staff', False):
            return True

        if self.superusers and getattr(user, 'is_superuser', False):
            return True

        if self.languages:
            languages = [ln.strip() for ln in self.languages.split(',')]
            if (hasattr(request, 'LANGUAGE_CODE') and
                    request.LANGUAGE_CODE in languages):
                return True

        users = cache.get(keyfmt(get_setting('FLAG_USERS_CACHE_KEY'),
                                             self.name))
        if users is None:
            users = self.users.all()
        # TODO: user.pk
        if user in users:
            return True

        groups = cache.get(keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'),
                                  self.name))
        if groups is None:
            groups = self.groups.all()
        user_groups = user.groups.all()
        for group in groups:
            if group in user_groups:
                return True

        if self.percent and self.percent > 0:
            if not hasattr(request, 'waffles'):
                request.waffles = {}
            elif self.name in request.waffles:
                return request.waffles[self.name][0]

            cookie = get_setting('COOKIE') % self.name
            if cookie in request.COOKIES:
                flag_active = (request.COOKIES[cookie] == 'True')
                set_flag(request, self.name, flag_active, self.rollout)
                return flag_active

            if Decimal(str(random.uniform(0, 100))) <= self.percent:
                set_flag(request, self.name, True, self.rollout)
                return True
            set_flag(request, self.name, False, self.rollout)

        return False


@python_2_unicode_compatible
class Switch(models.Model):
    """A feature switch.

    Switches are active, or inactive, globally.

    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    active = models.BooleanField(default=False, help_text=(
        'Is this switch active?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Switch is used.'))
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Switch was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Switch was last modified.'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Switch, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Switches'

    @classmethod
    def _cache_key(cls, name):
        return keyfmt(get_setting('SWITCH_CACHE_KEY'), name)

    @classmethod
    def get(cls, name):
        cache_key = cls._cache_key(name)
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return cls()
        if cached:
            return cached

        try:
            switch = cls.objects.get(name=name)
        except cls.DoesNotExist:
            cache.add(cache_key, CACHE_EMPTY)
            return cls()

        cache.add(cache_key, switch)
        return switch

    def is_active(self):
        if not self.pk:
            return get_setting('SWITCH_DEFAULT')
        return self.active


@python_2_unicode_compatible
class Sample(models.Model):
    """A sample is true some percentage of the time, but is not connected
    to users or requests.
    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    percent = models.DecimalField(max_digits=4, decimal_places=1, help_text=(
        'A number between 0.0 and 100.0 to indicate a percentage of the time '
        'this sample will be active.'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Sample is used.'))
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Sample was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Sample was last modified.'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Sample, self).save(*args, **kwargs)


def cache_flag(**kwargs):
    action = kwargs.get('action', None)
    # action is included for m2m_changed signal. Only cache on the post_*.
    if not action or action in ['post_add', 'post_remove', 'post_clear']:
        f = kwargs.get('instance')
        cache.add(keyfmt(get_setting('FLAG_CACHE_KEY'), f.name), f)
        cache.add(keyfmt(get_setting('FLAG_USERS_CACHE_KEY'), f.name),
                  f.users.all())
        cache.add(keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'), f.name),
                  f.groups.all())


def uncache_flag(**kwargs):
    flag = kwargs.get('instance')
    data = {
        keyfmt(get_setting('FLAG_CACHE_KEY'), flag.name): None,
        keyfmt(get_setting('FLAG_USERS_CACHE_KEY'), flag.name): None,
        keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'), flag.name): None,
        keyfmt(get_setting('ALL_FLAGS_CACHE_KEY')): None
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
    cache.add(keyfmt(get_setting('SAMPLE_CACHE_KEY'), sample.name), sample)


def uncache_sample(**kwargs):
    sample = kwargs.get('instance')
    cache.set(keyfmt(get_setting('SAMPLE_CACHE_KEY'), sample.name), None, 5)
    cache.set(keyfmt(get_setting('ALL_SAMPLES_CACHE_KEY')), None, 5)

post_save.connect(uncache_sample, sender=Sample, dispatch_uid='save_sample')
post_delete.connect(uncache_sample, sender=Sample,
                    dispatch_uid='delete_sample')


def cache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.add(keyfmt(get_setting('SWITCH_CACHE_KEY'), switch.name), switch)


def uncache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.set(keyfmt(get_setting('SWITCH_CACHE_KEY'), switch.name), None, 5)
    cache.set(keyfmt(get_setting('ALL_SWITCHES_CACHE_KEY')), None, 5)

post_delete.connect(uncache_switch, sender=Switch,
                    dispatch_uid='delete_switch')
post_save.connect(uncache_switch, sender=Switch, dispatch_uid='save_switch')
