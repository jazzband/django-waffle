from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from waffle.models import Flag


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--everyone',
            action='',
            dest='rollout_activate',
            help="Activate given target for feature."
        ),
        make_option('--deactivate',
            action='store_false',
            dest='rollout_activate',
            help="Deactivate given target for feature."
        )
    )
    help = "Modify a flag."
    args = "<flag_name>"

    def handle(self, flag_name=None, *args, **options):
        if not flag_name:
            raise CommandError('You need to specify a flag name.')

        try:
            flag = Flag.objects.get(name=flag_name)
            setattr(flag, attribute, value)
            flag.save()
        except Flag.DoesNotExist:
            raise CommandError('This flag doesn\'t exists')
