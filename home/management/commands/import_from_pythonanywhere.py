"""
Management command to import data from PythonAnywhere export.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Import data from PythonAnywhere export file'

    def add_arguments(self, parser):
        parser.add_argument(
            'fixture_file',
            type=str,
            help='Path to the JSON fixture file (vpq_data_export.json)'
        )

    def handle(self, *args, **options):
        fixture_file = options['fixture_file']

        if not os.path.exists(fixture_file):
            self.stdout.write(self.style.ERROR(f'File not found: {fixture_file}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Importing data from {fixture_file}...'))

        try:
            call_command('loaddata', fixture_file)
            self.stdout.write(self.style.SUCCESS('Successfully imported data from PythonAnywhere!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
            raise
