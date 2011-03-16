from django.contrib import admin

from waffle.models import Flag


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


admin.site.register(Flag, FlagAdmin)
