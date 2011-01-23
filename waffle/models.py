from django.contrib.auth.models import Group, User
from django.db import models


class Flag(models.Model):
    """A feature flag."""
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    everyone = models.NullBooleanField(blank=True, help_text=(
        'Turn this flag on (True) or off (False) for all users.'))
    percent = models.DecimalField(max_digits=3, decimal_places=1, null=True,
                                  blank=True, help_text=(
        'A number between 0.0 and 99.9 to indicate a percentage of users for '
        'whom this flag will be active.'))
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

    def __unicode__(self):
        return self.name
