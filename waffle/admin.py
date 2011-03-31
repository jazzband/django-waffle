from django.contrib import admin

from waffle.models import Flag, Switch


def enable_for_all(ma, request, qs):
    qs.update(everyone=True)
enable_for_all.short_description = 'Enable selected flags for everyone.'


def disable_for_all(ma, request, qs):
    qs.update(everyone=False)
disable_for_all.short_description = 'Disable selected flags for everyone.'


class FlagAdmin(admin.ModelAdmin):
    actions = [enable_for_all, disable_for_all]
    list_display = ('name', 'everyone', 'percent', 'superusers', 'staff',
                    'authenticated')
    list_filter = ('everyone', 'superusers', 'staff', 'authenticated')
    raw_id_fields = ('users', 'groups')


def enable_switches(ma, request, qs):
    qs.update(active=True)
enable_switches.short_description = 'Enable the selected switches.'


def disable_switches(ma, request, qs):
    qs.update(active=False)
disable_switches.short_description = 'Disable the selected switches.'


class SwitchAdmin(admin.ModelAdmin):
    actions = [enable_switches, disable_switches]
    list_display = ('name', 'active')
    list_filter = ('active',)


admin.site.register(Flag, FlagAdmin)
admin.site.register(Switch, SwitchAdmin)
