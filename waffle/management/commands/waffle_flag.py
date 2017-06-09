from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from waffle.models import Flag


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', nargs='?')
        parser.add_argument(
            '-l', '--list',
            action='store_true',
            dest='list_flags',
            default=False,
            help="List existing samples."),
        parser.add_argument(
            '--everyone',
            action='store_true',
            dest='everyone',
            help="Activate flag for all users."),
        parser.add_argument(
            '--deactivate',
            action='store_false',
            dest='everyone',
            help="Deactivate flag for all users."),
        parser.add_argument(
            '--percent', '-p',
            action='store',
            type=int,
            dest='percent',
            help='Roll out the flag for a certain percentage of users. Takes a number between 0.0 and 100.0'),
        parser.add_argument(
            '--superusers',
            action='store_true',
            dest='superusers',
            default=False,
            help='Turn on the flag for Django superusers.'),
        parser.add_argument(
            '--staff',
            action='store_true',
            dest='staff',
            default=False,
            help='Turn on the flag for Django staff.'),
        parser.add_argument(
            '--authenticated',
            action='store_true',
            dest='authenticated',
            default=False,
            help='Turn on the flag for logged in users.'),
        parser.add_argument(
            '--rollout', '-r',
            action='store_true',
            dest='rollout',
            default=False,
            help='Turn on rollout mode.'),
        parser.add_argument(
            '--create',
            action='store_true',
            dest='create',
            default=False,
            help='If the flag doesn\'t exist, create it.'),

    help = 'Modify a flag.'

    def handle(self, *args, **options):
        if options['list_flags']:
            self.stdout.write('Flags:')
            for flag in Flag.objects.iterator():
                self.stdout.write('NAME: %s' % flag.name)
                self.stdout.write('SUPERUSERS: %s' % flag.superusers)
                self.stdout.write('EVERYONE: %s' % flag.everyone)
                self.stdout.write('AUTHENTICATED: %s' % flag.authenticated)
                self.stdout.write('PERCENT: %s' % flag.percent)
                self.stdout.write('TESTING: %s' % flag.testing)
                self.stdout.write('ROLLOUT: %s' % flag.rollout)
                self.stdout.write('STAFF: %s' % flag.staff)
                self.stdout.write('')
            return

        flag_name = options['name']

        if options['create']:
            flag, created = Flag.objects.get_or_create(name=flag_name)
            if created:
                self.stdout.write('Creating flag: %s' % flag_name)
        else:
            try:
                flag = Flag.objects.get(name=flag_name)
            except Flag.DoesNotExist:
                raise CommandError("This flag doesn't exist")

        # Loop through all options, setting Flag attributes that
        # match (ie. don't want to try setting flag.verbosity)
        for option in options:
            if hasattr(flag, option):
                self.stdout.write('Setting %s: %s' % (option, options[option]))
                setattr(flag, option, options[option])

        flag.save()
