from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from waffle.models import Flag, Sample, Switch


def enable_for_all(ma, request, qs):
    # Iterate over all objects to cause cache invalidation.
    for f in qs.all():
        f.everyone = True
        f.save()
enable_for_all.short_description = 'Enable selected flags for everyone.'


def disable_for_all(ma, request, qs):
    # Iterate over all objects to cause cache invalidation.
    for f in qs.all():
        f.everyone = False
        f.save()
disable_for_all.short_description = 'Disable selected flags for everyone.'


class FlagForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(FlagForm, self).clean()

        active_for_cookie = cleaned_data.get('active_for_cookie', False)
        active_cookie_name = cleaned_data.get('active_cookie_name', '')
        active_cookie_value = cleaned_data.get('active_cookie_value', '')

        if active_for_cookie and not active_cookie_name:
            raise forms.ValidationError(
                '\'Active Cookie Name\' must be specified if using the'
                '\'Active For Cookie\' feature.'
            )
        elif active_cookie_value and not active_cookie_name:
            raise forms.ValidationError(
                '\'Active Cookie Name\' must be specified to use'
                ' \'Active Cookie Value\'.'
            )

        return cleaned_data

    class Meta:
        model = Flag
        exclude = []


class FlagAdmin(admin.ModelAdmin):
    actions = [enable_for_all, disable_for_all]
    date_hierarchy = 'created'
    list_display = ('name', 'note', 'everyone', 'percent', 'superusers',
                    'staff', 'authenticated', 'active_for_cookie', 'languages')
    list_filter = ('everyone', 'superusers', 'staff', 'authenticated', 'active_for_cookie')
    raw_id_fields = ('users', 'groups')
    ordering = ('-id',)
    form = FlagForm

    fieldsets = [
        (
            None,
            {
                'fields': [
                    'name',
                    'everyone',
                    'percent',
                    'testing',
                    'superusers',
                    'staff',
                    'authenticated',
                    'languages',
                    'groups',
                    'users',
                    ('active_for_cookie', 'active_cookie_name', 'active_cookie_value',),
                    'rollout',
                    'note',
                    'created',
                    'modified'
                ],
            }
        )
    ]


def enable_switches(ma, request, qs):
    for switch in qs:
        switch.active = True
        switch.save()
enable_switches.short_description = 'Enable the selected switches.'


def disable_switches(ma, request, qs):
    for switch in qs:
        switch.active = False
        switch.save()
disable_switches.short_description = 'Disable the selected switches.'


class SwitchAdmin(admin.ModelAdmin):
    actions = [enable_switches, disable_switches]
    date_hierarchy = 'created'
    list_display = ('name', 'active', 'note', 'created', 'modified')
    list_filter = ('active',)
    ordering = ('-id',)


class SampleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name', 'percent', 'note', 'created', 'modified')
    ordering = ('-id',)


admin.site.register(Flag, FlagAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Switch, SwitchAdmin)
