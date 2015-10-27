try:
    from django.utils import timezone as datetime
except ImportError:
    from datetime import datetime

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed

from waffle.compat import AUTH_USER_MODEL, cache
from waffle.utils import get_setting, keyfmt


class Flag(models.Model):
    """A feature flag.

    Flags are active (or not) on a per-request basis.

    """
    name = models.CharField(max_length=100,
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
    users = models.ManyToManyField(AUTH_USER_MODEL, blank=True, help_text=(
        'Activate this flag for these users.'))
    rollout = models.BooleanField(default=False, help_text=(
        'Activate roll-out mode?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Flag is used.'))
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Flag was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Flag was last modified.'))

    site = models.ForeignKey(Site, blank=True, null=True, related_name='waffle_flags')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Flag, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'site')

class Switch(models.Model):
    """A feature switch.

    Switches are active, or inactive, globally.

    """
    name = models.CharField(max_length=100, 
                            help_text='The human/computer readable name.')
    active = models.BooleanField(default=False, help_text=(
        'Is this flag active?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Switch is used.'))
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Switch was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Switch was last modified.'))

    site = models.ForeignKey(Site, blank=True, null=True, related_name='waffle_switches')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Switch, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Switches'
        unique_together = ('name', 'site')


class Sample(models.Model):
    """A sample is true some percentage of the time, but is not connected
    to users or requests.
    """
    name = models.CharField(max_length=100,
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

    site = models.ForeignKey(Site, blank=True, null=True, related_name='waffle_samples')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Sample, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'site')

def cache_flag(**kwargs):
    action = kwargs.get('action', None)
    # action is included for m2m_changed signal. Only cache on the post_*.
    if not action or action in ['post_add', 'post_remove', 'post_clear']:
        f = kwargs.get('instance')
        cache.add(keyfmt(get_setting('FLAG_CACHE_KEY'), f.name, f.site), f)
        cache.add(keyfmt(get_setting('FLAG_USERS_CACHE_KEY'), f.name, f.site),
                  f.users.all())
        cache.add(keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'), f.name, f.site),
                  f.groups.all())


def uncache_flag(**kwargs):
    flag = kwargs.get('instance')
    data = [
        keyfmt(get_setting('FLAG_CACHE_KEY'), flag.name, flag.site),
        keyfmt(get_setting('FLAG_USERS_CACHE_KEY'), flag.name, flag.site),
        keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'), flag.name, flag.site),
        keyfmt(get_setting('ALL_FLAGS_CACHE_KEY'))
    ]
    cache.delete_many(data)

post_save.connect(uncache_flag, sender=Flag, dispatch_uid='save_flag')
post_delete.connect(uncache_flag, sender=Flag, dispatch_uid='delete_flag')
m2m_changed.connect(uncache_flag, sender=Flag.users.through,
                    dispatch_uid='m2m_flag_users')
m2m_changed.connect(uncache_flag, sender=Flag.groups.through,
                    dispatch_uid='m2m_flag_groups')


def cache_sample(**kwargs):
    sample = kwargs.get('instance')
    cache.add(keyfmt(get_setting('SAMPLE_CACHE_KEY'), sample.name, sample.site), sample)


def uncache_sample(**kwargs):
    sample = kwargs.get('instance')
    cache.set(keyfmt(get_setting('SAMPLE_CACHE_KEY'), sample.name, sample.site), None, 5)
    cache.delete(keyfmt(get_setting('ALL_SAMPLES_CACHE_KEY')))

post_save.connect(uncache_sample, sender=Sample, dispatch_uid='save_sample')
post_delete.connect(uncache_sample, sender=Sample,
                    dispatch_uid='delete_sample')


def cache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.add(keyfmt(get_setting('SWITCH_CACHE_KEY'), switch.name, switch.site), switch)


def uncache_switch(**kwargs):
    switch = kwargs.get('instance')
    cache.delete(keyfmt(get_setting('SWITCH_CACHE_KEY'), switch.name, switch.site))
    cache.delete(keyfmt(get_setting('ALL_SWITCHES_CACHE_KEY')))

post_delete.connect(uncache_switch, sender=Switch,
                    dispatch_uid='delete_switch')
post_save.connect(uncache_switch, sender=Switch, dispatch_uid='save_switch')
