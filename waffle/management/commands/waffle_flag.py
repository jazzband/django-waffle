from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.models import Q

from waffle import get_waffle_flag_model

UserModel = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'name',
            nargs='?',
            help='The name of the flag.')
        parser.add_argument(
            '-l', '--list',
            action='store_true',
            dest='list_flags',
            default=False,
            help='List existing samples.')
        parser.add_argument(
            '--everyone',
            action='store_true',
            dest='everyone',
            help='Activate flag for all users.')
        parser.add_argument(
            '--deactivate',
            action='store_false',
            dest='everyone',
            help='Deactivate flag for all users.')
        parser.add_argument(
            '--percent', '-p',
            action='store',
            type=int,
            dest='percent',
            help='Roll out the flag for a certain percentage of users. Takes '
                 'a number between 0.0 and 100.0')
        parser.add_argument(
            '--superusers',
            action='store_true',
            dest='superusers',
            default=False,
            help='Turn on the flag for Django superusers.')
        parser.add_argument(
            '--staff',
            action='store_true',
            dest='staff',
            default=False,
            help='Turn on the flag for Django staff.')
        parser.add_argument(
            '--authenticated',
            action='store_true',
            dest='authenticated',
            default=False,
            help='Turn on the flag for logged in users.')
        parser.add_argument(
            '--group', '-g',
            action='append',
            default=list(),
            help='Turn on the flag for listed group names (use flag more '
                 'than once for multiple groups). WARNING: This will remove '
                 'any currently associated groups unless --append is used!')
        parser.add_argument(
            '--user', '-u',
            action='append',
            default=list(),
            help='Turn on the flag for listed usernames (use flag more '
                 'than once for multiple users). WARNING: This will remove '
                 'any currently associated users unless --append is used!')
        parser.add_argument(
            '--append',
            action='store_true',
            dest='append',
            default=False,
            help='Append only mode when adding groups.')
        parser.add_argument(
            '--rollout', '-r',
            action='store_true',
            dest='rollout',
            default=False,
            help='Turn on rollout mode.')
        parser.add_argument(
            '--testing', '-t',
            action='store_true',
            dest='testing',
            default=False,
            help='Turn on testing mode, allowing the flag to be specified via '
                 'a querystring parameter.')
        parser.add_argument(
            '--create',
            action='store_true',
            dest='create',
            default=False,
            help='If the flag doesn\'t exist, create it.')
        parser.set_defaults(everyone=None)

    help = 'Modify a flag.'

    def handle(self, *args: Any, **options: Any) -> None:
        if options['list_flags']:
            self.stdout.write('Flags:')
            for flag in get_waffle_flag_model().objects.iterator():
                self.log_flag_to_stdout(flag)
            return

        flag_name = options['name']

        if not flag_name:
            raise CommandError('You need to specify a flag name.')

        if options['create']:
            flag, created = get_waffle_flag_model().objects.get_or_create(name=flag_name)
            if created:
                self.stdout.write(f'Creating flag: {flag_name}')
        else:
            try:
                flag = get_waffle_flag_model().objects.get(name=flag_name)
            except get_waffle_flag_model().DoesNotExist:
                raise CommandError('This flag does not exist.')

        # Group isn't an attribute on the Flag, but a related Many-to-Many
        # field, so we handle it a bit differently by looking up groups and
        # adding each group to the flag individually
        options_append = options.pop('append')
        if groups := options.pop('group'):
            group_hash = {}
            for group in groups:
                try:
                    group_instance = Group.objects.get(name=group)
                    group_hash[group_instance.name] = group_instance.id
                except Group.DoesNotExist:
                    raise CommandError(f'Group {group} does not exist')
            # If 'append' was not passed, we clear related groups
            if not options_append:
                flag.groups.clear()
            self.stdout.write('Setting group(s): %s' % (
                [name for name, _id in group_hash.items()])
                              )
            for group_id in group_hash.values():
                flag.groups.add(group_id)
        if users := options.pop('user'):
            user_hash = set()
            for username in users:
                try:
                    user_instance = UserModel.objects.get(
                        Q(**{UserModel.USERNAME_FIELD: username})
                        | Q(**{UserModel.EMAIL_FIELD: username})
                    )
                    user_hash.add(user_instance)
                except UserModel.DoesNotExist:
                    raise CommandError(f'User {username} does not exist')
            # If 'append' was not passed, we clear related users
            if not options_append:
                flag.users.clear()
            self.stdout.write(f'Setting user(s): {user_hash}')
            # for user in user_hash:
            flag.users.add(*[user.id for user in user_hash])
        for option_name, option in options.items():
            if hasattr(flag, option_name):
                self.stdout.write(f'Setting {option_name}: {option}')
                setattr(flag, option_name, option)

        flag.save()

    def log_flag_to_stdout(self, flag):
        self.stdout.write(f'NAME: {flag.name}')
        self.stdout.write(f'SUPERUSERS: {flag.superusers}')
        self.stdout.write(f'EVERYONE: {flag.everyone}')
        self.stdout.write(f'AUTHENTICATED: {flag.authenticated}')
        self.stdout.write(f'PERCENT: {flag.percent}')
        self.stdout.write(f'TESTING: {flag.testing}')
        self.stdout.write(f'ROLLOUT: {flag.rollout}')
        self.stdout.write(f'STAFF: {flag.staff}')
        self.stdout.write('GROUPS: {}'.format(list(
            flag.groups.values_list('name', flat=True)))
        )
        self.stdout.write('USERS: {}'.format(list(
            flag.users.values_list(UserModel.USERNAME_FIELD, flat=True)))
        )
        self.stdout.write('')
