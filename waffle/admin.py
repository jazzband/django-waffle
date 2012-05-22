from django.contrib import admin

from waffle.models import Flag, Sample, Switch


def enable_for_all(ma, request, qs):
    qs.update(everyone=True)
enable_for_all.short_description = 'Enable selected flags for everyone.'


def disable_for_all(ma, request, qs):
    qs.update(everyone=False)
disable_for_all.short_description = 'Disable selected flags for everyone.'


class FlagAdmin(admin.ModelAdmin):
    actions = [enable_for_all, disable_for_all]
    date_hierarchy = 'created'
    list_display = ('name', 'everyone', 'percent', 'superusers', 'staff',
                    'authenticated', 'note')
    list_filter = ('everyone', 'superusers', 'staff', 'authenticated',
                   'created', 'modified')
    raw_id_fields = ('users', 'groups')
    ordering = ('-id',)


def enable_switches(ma, request, qs):
    for switch in qs:
        switch.active=True
        switch.save()
enable_switches.short_description = 'Enable the selected switches.'


def disable_switches(ma, request, qs):
    for switch in qs:
        switch.active=False
        switch.save()
disable_switches.short_description = 'Disable the selected switches.'


class SwitchAdmin(admin.ModelAdmin):
    actions = [enable_switches, disable_switches]
    date_hierarchy = 'created'
    list_display = ('name', 'active', 'created', 'modified', 'note')
    list_filter = ('active',)
    ordering = ('-id',)


class SampleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name', 'percent', 'created', 'modified', 'note')
    ordering = ('-id',)


admin.site.register(Flag, FlagAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Switch, SwitchAdmin)
