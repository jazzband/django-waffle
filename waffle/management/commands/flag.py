from __future__ import print_function

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from waffle.models import Flag


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-l', '--list',
            action='store_true',
            dest='list_flag',
            default=False,
            help="List existing samples."),
        make_option('--everyone',
            action='store_true',
            dest='everyone',
            help="Activate flag for all users."),
        make_option('--deactivate',
            action='store_false',
            dest='everyone',
            help="Deactivate flag for all users."),
        make_option('--percent', '-p',
            action='store',
            type='int',
            dest='percent',
            help=('Roll out the flag for a certain percentage of users. '
                  'Takes a number between 0.0 and 100.0')),
        make_option('--superusers',
            action='store_true',
            dest='superusers',
            default=False,
            help='Turn on the flag for Django superusers.'),
        make_option('--staff',
            action='store_true',
            dest='staff',
            default=False,
            help='Turn on the flag for Django staff.'),
        make_option('--authenticated',
            action='store_true',
            dest='authenticated',
            default=False,
            help='Turn on the flag for logged in users.'),
        make_option('--rollout', '-r',
            action='store_true',
            dest='rollout',
            default=False,
            help='Turn on rollout mode.'),
        make_option('--create',
            action='store_true',
            dest='create',
            default=False,
            help='If the flag doesn\'t exist, create it.'),
    )

    help = "Modify a flag."
    args = "<flag_name>"

    def handle(self, flag_name=None, *args, **options):
        list_flag = options['list_flag']

        if list_flag:
            print('Flags:')
            for flag in Flag.objects.iterator():
                print('\nNAME: %s' % flag.name)
                print('SUPERUSERS: %s' % flag.superusers)
                print('EVERYONE: %s' % flag.everyone)
                print('AUTHENTICATED: %s' % flag.authenticated)
                print('PERCENT: %s' % flag.percent)
                print('TESTING: %s' % flag.testing)
                print('ROLLOUT: %s' % flag.rollout)
                print('STAFF: %s' % flag.staff)
            return

        if not flag_name:
            raise CommandError("You need to specify a flag name.")

        if options['create']:
            flag, created = Flag.objects.get_or_create(name=flag_name)
            if created:
                print('Creating flag: %s' % flag_name)
        else:
            try:
                flag = Flag.objects.get(name=flag_name)
            except Flag.DoesNotExist:
                raise CommandError("This flag doesn't exist")

        # Loop through all options, setting Flag attributes that
        # match (ie. don't want to try setting flag.verbosity)
        for option in options:
            if hasattr(flag, option):
                print('Setting %s: %s' % (option, options[option]))
                setattr(flag, option, options[option])

        flag.save()
