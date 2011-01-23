from django.contrib import admin

from waffles.models import Flag


class FlagAdmin(admin.ModelAdmin):
    list_display = ('name', 'everyone', 'percent', 'superusers', 'staff',
                    'authenticated')
    list_filter = ('everyone', 'superusers', 'staff', 'authenticated')
    raw_id_fields = ('users', 'groups')


admin.site.register(Flag, FlagAdmin)
