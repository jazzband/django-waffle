from django.contrib import admin

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


class FlagAdmin(admin.ModelAdmin):
    actions = [enable_for_all, disable_for_all]
    date_hierarchy = 'created'
    list_display = ('name', 'site', 'note', 'everyone', 'percent', 'superusers',
                    'staff', 'authenticated', 'languages')
    list_filter = ('site', 'everyone', 'superusers', 'staff', 'authenticated')
    raw_id_fields = ('users', 'groups')
    ordering = ('-id',)


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
    list_display = ('name', 'site', 'active', 'note', 'created', 'modified')
    list_filter = ('site', 'active',)
    ordering = ('-id',)


class SampleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name', 'site', 'percent', 'note', 'created', 'modified')
    list_filter = ('site', )
    ordering = ('-id',)


admin.site.register(Flag, FlagAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Switch, SwitchAdmin)
