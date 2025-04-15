# In a file management/commands/populate_departments.py
from django.core.management.base import BaseCommand
from undrid.management.commands.seed import populate_departments # Import the function


class Command(BaseCommand):
    help = 'Populate departments in database'

    def handle(self, *args, **options):
        created, skipped, errors = populate_departments()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} departments'))
        if skipped:
            self.stdout.write(self.style.WARNING(f'Skipped {skipped} departments'))
        if errors:
            self.stdout.write(self.style.ERROR(f'Encountered {errors} errors'))