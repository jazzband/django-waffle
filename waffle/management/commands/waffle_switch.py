from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from waffle.models import Switch


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-l', '--list',
                            action='store_true', dest='list_switch', default=False,
                            help='List existing switchs.')
        parser.add_argument('--create',
                            action='store_true',
                            dest='create',
                            default=False,
                            help="If the switch doesn't exist, create it.")
        parser.add_argument('switch_name', nargs='?', type=str)
        parser.add_argument('state', nargs='?', type=str)

    help = 'Activate or deactivate a switch.'
    args = '<switch_name> <on/off>'

    def handle(self, *args, **options):
        list_switch = options['list_switch']
        switch_name = options['switch_name']
        state = options['state']
        if list_switch:
            print('Switches:')
            for switch in Switch.objects.iterator():
                print('%s: %s' % (switch.name,
                                  'on' if switch.active else 'off'))
            return

        if not (switch_name and state):
            raise CommandError('You need to specify a switch name and state.')

        if not state in ['on', 'off']:
            raise CommandError('You need to specify state of switch with '
                               '"on" or "off".')

        if options['create']:
            switch, created = Switch.objects.get_or_create(name=switch_name)
            if created:
                print('Creating switch: %s' % switch_name)
        else:
            try:
                switch = Switch.objects.get(name=switch_name)
            except Switch.DoesNotExist:
                raise CommandError("This switch doesn't exist.")

        switch.active = state == "on"
        switch.save()
