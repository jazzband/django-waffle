from django.core.management.base import BaseCommand, CommandError

from waffle.models import Switch


class Command(BaseCommand):
    help = "Activate or deactivate a switch."
    args = "<switch_name> <on/off>"

    def handle(self, switch_name=None, state=None, *args, **options):
        if not (switch_name and state):
            raise CommandError('You need to specify a switch name and his state.')

        if not state in ["on", "off"]:
            raise CommandError('You need to specify state of switch with "on" or "off"')

        try:
            switch = Switch.objects.get(name=switch_name)
            switch.active = state == "on"
            switch.save()
        except Switch.DoesNotExist:
            raise CommandError('This switch doesn\'t exists')
