from __future__ import unicode_literals

import random
from decimal import Decimal

try:
    from django.utils import timezone as datetime
except ImportError:
    from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models, router
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from waffle import managers
from waffle.utils import get_setting, keyfmt, get_cache, is_authenticated

cache = get_cache()
CACHE_EMPTY = '-'


@python_2_unicode_compatible
class BaseModel(models.Model):
    SINGLE_CACHE_KEY = ''
    ALL_CACHE_KEY = ''

    class Meta(object):
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def _cache_key(cls, name):
        return keyfmt(get_setting(cls.SINGLE_CACHE_KEY), name)

    @classmethod
    def get(cls, name):
        cache_key = cls._cache_key(name)
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return cls()
        if cached:
            return cached

        try:
            obj = cls.get_from_db(name)
        except cls.DoesNotExist:
            cache.add(cache_key, CACHE_EMPTY)
            return cls()

        cache.add(cache_key, obj)
        return obj

    @classmethod
    def get_from_db(cls, name):
        objects = cls.objects
        if get_setting('READ_FROM_WRITE_DB'):
            objects = objects.using(router.db_for_write(cls))
        return objects.get(name=name)

    @classmethod
    def get_all(cls):
        cache_key = get_setting(cls.ALL_CACHE_KEY)
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return []
        if cached:
            return cached

        objs = cls.get_all_from_db()
        if not objs:
            cache.add(cache_key, CACHE_EMPTY)
            return []

        cache.add(cache_key, objs)
        return objs

    @classmethod
    def get_all_from_db(cls):
        objects = cls.objects
        if get_setting('READ_FROM_WRITE_DB'):
            objects = objects.using(router.db_for_write(cls))
        return list(objects.all())

    def flush(self):
        keys = [
            self._cache_key(self.name),
            get_setting(self.ALL_CACHE_KEY),
        ]
        cache.delete_many(keys)

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        ret = super(BaseModel, self).save(*args, **kwargs)
        self.flush()
        return ret

    def delete(self, *args, **kwargs):
        ret = super(BaseModel, self).delete(*args, **kwargs)
        self.flush()
        return ret


def set_flag(request, flag_name, active=True, session_only=False):
    """Set a flag value on a request object."""
    if not hasattr(request, 'waffles'):
        request.waffles = {}
    request.waffles[flag_name] = [active, session_only]


class Flag(BaseModel):
    """A feature flag.

    Flags are active (or not) on a per-request basis.

    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('The human/computer readable name.'),
        verbose_name=_('Name'),
    )
    everyone = models.NullBooleanField(
        blank=True,
        help_text=_(
            'Flip this flag on (Yes) or off (No) for everyone, overriding all '
            'other settings. Leave as Unknown to use normally.'),
        verbose_name=_('Everyone'),
    )
    percent = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_('A number between 0.0 and 99.9 to indicate a percentage of '
                    'users for whom this flag will be active.'),
        verbose_name=_('Percent'),
    )
    testing = models.BooleanField(
        default=False,
        help_text=_('Allow this flag to be set for a session for user testing'),
        verbose_name=_('Testing'),
    )
    superusers = models.BooleanField(
        default=True,
        help_text=_('Flag always active for superusers?'),
        verbose_name=_('Superusers'),
    )
    staff = models.BooleanField(
        default=False,
        help_text=_('Flag always active for staff?'),
        verbose_name=_('Staff'),
    )
    authenticated = models.BooleanField(
        default=False,
        help_text=_('Flag always active for authenticated users?'),
        verbose_name=_('Authenticated'),
    )
    languages = models.TextField(
        blank=True,
        default='',
        help_text=_('Activate this flag for users with one of these languages (comma-separated list)'),
        verbose_name=_('Languages'),
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=_('Activate this flag for these user groups.'),
        verbose_name=_('Groups'),
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        help_text=_('Activate this flag for these users.'),
        verbose_name=_('Users'),
    )
    rollout = models.BooleanField(
        default=False,
        help_text=_('Activate roll-out mode?'),
        verbose_name=_('Rollout'),
    )
    note = models.TextField(
        blank=True,
        help_text=_('Note where this Flag is used.'),
        verbose_name=_('Note'),
    )
    created = models.DateTimeField(
        default=datetime.now,
        db_index=True,
        help_text=_('Date when this Flag was created.'),
        verbose_name=_('Created'),
    )
    modified = models.DateTimeField(
        default=datetime.now,
        help_text=_('Date when this Flag was last modified.'),
        verbose_name=_('Modified'),
    )

    objects = managers.FlagManager()

    SINGLE_CACHE_KEY = 'FLAG_CACHE_KEY'
    ALL_CACHE_KEY = 'ALL_FLAGS_CACHE_KEY'

    class Meta:
        verbose_name = _('Flag')
        verbose_name_plural = _('Flags')

    def flush(self):
        keys = [
            self._cache_key(self.name),
            keyfmt(get_setting('FLAG_USERS_CACHE_KEY'), self.name),
            keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'), self.name),
            get_setting('ALL_FLAGS_CACHE_KEY'),
        ]
        cache.delete_many(keys)

    def _get_user_ids(self):
        cache_key = keyfmt(get_setting('FLAG_USERS_CACHE_KEY'), self.name)
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return set()
        if cached:
            return cached

        user_ids = set(self.users.all().values_list('pk', flat=True))
        if not user_ids:
            cache.add(cache_key, CACHE_EMPTY)
            return set()

        cache.add(cache_key, user_ids)
        return user_ids

    def _get_group_ids(self):
        cache_key = keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'), self.name)
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return set()
        if cached:
            return cached

        group_ids = set(self.groups.all().values_list('pk', flat=True))
        if not group_ids:
            cache.add(cache_key, CACHE_EMPTY)
            return set()

        cache.add(cache_key, group_ids)
        return group_ids

    def is_active_for_user(self, user):
        authed = is_authenticated(user)

        if self.authenticated and authed:
            return True

        if self.staff and getattr(user, 'is_staff', False):
            return True

        if self.superusers and getattr(user, 'is_superuser', False):
            return True

        user_ids = self._get_user_ids()
        if hasattr(user, 'pk') and user.pk in user_ids:
            return True

        if hasattr(user, 'groups'):
            group_ids = self._get_group_ids()
            user_groups = set(user.groups.all().values_list('pk', flat=True))
            if group_ids.intersection(user_groups):
                return True
        return None

    def _is_active_for_user(self, request):
        return self.is_active_for_user(request.user)

    def _is_active_for_language(self, request):
        if self.languages:
            languages = [ln.strip() for ln in self.languages.split(',')]
            if (hasattr(request, 'LANGUAGE_CODE') and
                    request.LANGUAGE_CODE in languages):
                return True
        return None

    def is_active(self, request):
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

        active_for_language = self._is_active_for_language(request)
        if active_for_language is not None:
            return active_for_language

        active_for_user = self._is_active_for_user(request)
        if active_for_user is not None:
            return active_for_user

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


class Switch(BaseModel):
    """A feature switch.

    Switches are active, or inactive, globally.

    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('The human/computer readable name.'),
        verbose_name=_('Name'),
    )
    active = models.BooleanField(
        default=False,
        help_text=_('Is this switch active?'),
        verbose_name=_('Active'),
    )
    note = models.TextField(
        blank=True,
        help_text=_('Note where this Switch is used.'),
        verbose_name=_('Note'),
    )
    created = models.DateTimeField(
        default=datetime.now,
        db_index=True,
        help_text=_('Date when this Switch was created.'),
        verbose_name=_('Created'),
    )
    modified = models.DateTimeField(
        default=datetime.now,
        help_text=_('Date when this Switch was last modified.'),
        verbose_name=_('Modified'),
    )

    objects = managers.SwitchManager()

    SINGLE_CACHE_KEY = 'SWITCH_CACHE_KEY'
    ALL_CACHE_KEY = 'ALL_SWITCHES_CACHE_KEY'

    class Meta:
        verbose_name = _('Switch')
        verbose_name_plural = _('Switches')

    def is_active(self):
        if not self.pk:
            return get_setting('SWITCH_DEFAULT')
        return self.active


class Sample(BaseModel):
    """A sample of users.

    A sample is true some percentage of the time, but is not connected
    to users or requests.

    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('The human/computer readable name.'),
        verbose_name=_('Name'),
    )
    percent = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text=_('A number between 0.0 and 100.0 to indicate a percentage of the time '
                    'this sample will be active.'),
        verbose_name=_('Percent'),
    )
    note = models.TextField(
        blank=True,
        help_text=_('Note where this Sample is used.'),
        verbose_name=_('Note'),
    )
    created = models.DateTimeField(
        default=datetime.now,
        db_index=True,
        help_text=_('Date when this Sample was created.'),
        verbose_name=_('Created'),
    )
    modified = models.DateTimeField(
        default=datetime.now,
        help_text=_('Date when this Sample was last modified.'),
        verbose_name=_('Modified'),
    )

    objects = managers.SampleManager()

    SINGLE_CACHE_KEY = 'SAMPLE_CACHE_KEY'
    ALL_CACHE_KEY = 'ALL_SAMPLES_CACHE_KEY'

    class Meta:
        verbose_name = _('Sample')
        verbose_name_plural = _('Samples')

    def is_active(self):
        if not self.pk:
            return get_setting('SAMPLE_DEFAULT')
        return Decimal(str(random.uniform(0, 100))) <= self.percent
