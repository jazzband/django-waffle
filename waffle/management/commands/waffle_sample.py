from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from waffle.models import Sample


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('positionals', nargs='*')
        parser.add_argument(
            '-l', '--list',
            action='store_true', dest='list_samples', default=False,
            help='List existing samples.'),
        parser.add_argument(
            '--create',
            action='store_true',
            dest='create',
            default=False,
            help="If the sample doesn't exist, create it."),

    help = 'Change percentage of a sample.'

    def handle(self, *args, **options):
        if options['list_samples']:
            self.stdout.write('Samples:')
            for sample in Sample.objects.iterator():
                self.stdout.write('%s: %s%%' % (sample.name, sample.percent))
            self.stdout.write('')
            return

        sample_name = options['positionals'][0]
        percent = options['positionals'][1]

        if not (sample_name and percent):
            raise CommandError('You need to specify a sample name and percentage.')

        try:
            percent = float(percent)
            if not (0.0 <= percent <= 100.0):
                raise ValueError()
        except ValueError:
            raise CommandError('You need to enter a valid percentage value.')

        if options['create']:
            sample, created = Sample.objects.get_or_create(
                name=sample_name, defaults={'percent': 0})
            if created:
                self.stdout.write('Creating sample: %s' % sample_name)
        else:
            try:
                sample = Sample.objects.get(name=sample_name)
            except Sample.DoesNotExist:
                raise CommandError('This sample does not exist.')

        sample.percent = percent
        sample.save()
