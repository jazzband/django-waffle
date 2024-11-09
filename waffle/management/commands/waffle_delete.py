from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from waffle import (
    get_waffle_flag_model,
    get_waffle_switch_model,
    get_waffle_sample_model,
)


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--flags',
            action='store',
            dest='flag_names',
            nargs='*',
            help='List of flag names to delete.')
        parser.add_argument(
            '--samples',
            action='store',
            dest='sample_names',
            nargs='*',
            help='List of sample names to delete.')
        parser.add_argument(
            '--switches',
            action='store',
            dest='switch_names',
            nargs='*',
            help='List of switch names to delete.')

    help = 'Delete flags, samples, and switches from database'

    def handle(self, *args: Any, **options: Any) -> None:
        if flags := options['flag_names']:
            flag_queryset = get_waffle_flag_model().objects.filter(name__in=flags)
            flag_count = flag_queryset.count()
            flag_queryset.delete()
            self.stdout.write(f'Deleted {flag_count} Flags')

        if switches := options['switch_names']:
            switches_queryset = get_waffle_switch_model().objects.filter(
                name__in=switches
            )
            switch_count = switches_queryset.count()
            switches_queryset.delete()
            self.stdout.write(f'Deleted {switch_count} Switches')

        if samples := options['sample_names']:
            sample_queryset = get_waffle_sample_model().objects.filter(name__in=samples)
            sample_count = sample_queryset.count()
            sample_queryset.delete()
            self.stdout.write(f'Deleted {sample_count} Samples')
