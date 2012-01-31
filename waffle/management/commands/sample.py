from django.core.management.base import BaseCommand, CommandError

from waffle.models import Sample


class Command(BaseCommand):
    help = "Change percentage of a sample."
    args = "<sample_name> <percent>"

    def handle(self, sample_name=None, percent=None, *args, **options):
        if not (sample_name and percent):
            raise CommandError('You need to specify a sample name and percentage.')

        try:
            percent = float(percent)
            if not (0.0 <= percent <= 100.0):
                raise ValueError()
        except ValueError:
            raise CommandError('You need to enter a valid percentage value')

        try:
            sample = Sample.objects.get(name=sample_name)
            sample.percent = percent
            sample.save()
        except Sample.DoesNotExist:
            raise CommandError('This sample doesn\'t exist')
