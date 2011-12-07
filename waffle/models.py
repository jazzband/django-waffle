from datetime import datetime

from django.contrib.auth.models import Group, User
from django.db import models


class Flag(models.Model):
    """A feature flag.

    Flags are active (or not) on a per-request basis.

    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    everyone = models.NullBooleanField(blank=True, help_text=(
        'Turn this flag on (True) or off (False) for all users.'))
    percent = models.DecimalField(max_digits=3, decimal_places=1, null=True,
                                  blank=True, help_text=(
        'A number between 0.0 and 99.9 to indicate a percentage of users for '
        'whom this flag will be active.'))
    testing = models.BooleanField(default=False, help_text=(
        'Allow this flag to be set for a session for user testing.'))
    superusers = models.BooleanField(default=True, help_text=(
        'Activate this flag for superusers?'))
    staff = models.BooleanField(default=False, help_text=(
        'Activate this flag for staff?'))
    authenticated = models.BooleanField(default=False, help_text=(
        'Activate this flag for authenticate users?'))
    groups = models.ManyToManyField(Group, blank=True, help_text=(
        'Activate this flag for these user groups.'))
    users = models.ManyToManyField(User, blank=True, help_text=(
        'Activate this flag for these users.'))
    rollout = models.BooleanField(default=False, help_text=(
        'Activate roll-out mode?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Flag is used.'))
    created = models.DateTimeField(auto_now_add=True, db_index=True,
        help_text=('Date when this Flag was created.'))
    modified = models.DateTimeField(auto_now=True, help_text=(
        'Date when this Flag was last modified.'))

    def __unicode__(self):
        return self.name


class Switch(models.Model):
    """A feature switch.

    Switches are active, or inactive, globally.

    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    active = models.BooleanField(default=False, help_text=(
        'Is this flag active?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Switch is used.'))
    created = models.DateTimeField(auto_now_add=True, db_index=True,
        help_text=('Date when this Switch was created.'))
    modified = models.DateTimeField(auto_now=True, help_text=(
        'Date when this Switch was last modified.'))

    def __unicode__(self):
        return u'%s: %s' % (self.name, 'on' if self.active else 'off')

    class Meta:
        verbose_name_plural = 'Switches'


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
    created = models.DateTimeField(auto_now_add=True, db_index=True,
        help_text=('Date when this Sample was created.'))
    modified = models.DateTimeField(auto_now=True, help_text=(
        'Date when this Sample was last modified.'))

    def __unicode__(self):
        return self.name
