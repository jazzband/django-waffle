from django.core.management.base import BaseCommand, CommandError

from waffle.models import Switch


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('positionals', nargs='*')
        parser.add_argument(
            '-l', '--list',
            action='store_true', dest='list_switches', default=False,
            help='List existing switches.'),
        parser.add_argument(
            '--create',
            action='store_true',
            dest='create',
            default=False,
            help="If the switch doesn't exist, create it."),

    help = 'Activate or deactivate a switch.'

    def handle(self, *args, **options):
        if options['list_switches']:
            self.stdout.write('Switches:')
            for switch in Switch.objects.iterator():
                self.stdout.write('%s: %s' % (switch.name, 'on' if switch.active else 'off'))
            self.stdout.write('')
            return

        switch_name = options['positionals'][0]
        state = options['positionals'][1]
        print(options['positionals'])

        if not (switch_name and state):
            raise CommandError('You need to specify a switch name and state.')

        if state not in ['on', 'off']:
            raise CommandError('You need to specify state of switch with "on" or "off".')

        active = state == "on"
        defaults = {'active': active}

        if options['create']:
            switch, created = Switch.objects.get_or_create(name=switch_name, defaults=defaults)
            if created:
                self.stdout.write('Creating switch: %s' % switch_name)
        else:
            try:
                switch = Switch.objects.update_or_create(name=switch_name, defaults=defaults)
            except Switch.DoesNotExist:
                raise CommandError("This switch doesn't exist.")
