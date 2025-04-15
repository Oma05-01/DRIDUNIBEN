import os
from django.core.management.base import BaseCommand
from undrid.models import * # Adjust if app name differs

class Command(BaseCommand):
    help = "Import faculties and departments from a structured text file"

    def handle(self, *args, **options):
        file_path = os.path.join('List of Faculties and Depts.txt')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            current_faculty = None
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if not line.startswith('-'):
                    # New Faculty
                    current_faculty, created = Faculty.objects.get_or_create(name=line)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created Faculty: {line}"))
                    else:
                        self.stdout.write(f"Faculty exists: {line}")
                else:
                    # New Department under current faculty
                    dept_name = line.lstrip('-').strip()
                    if current_faculty:
                        dept_obj, created = Department.objects.get_or_create(
                            name=dept_name,
                            faculty=current_faculty
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"  Added Dept: {dept_name}"))
                        else:
                            self.stdout.write(f"  Dept exists: {dept_name}")
