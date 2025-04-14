from django.core.management.base import BaseCommand
from undrid.models import Faculty, Department
import re


class Command(BaseCommand):
    help = 'Import university structure data from the provided text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'r') as file:
                content = file.read()

            # Process the file content
            self.import_data(content)
            self.stdout.write(self.style.SUCCESS('Successfully imported university data'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))

    def import_data(self, content):
        # Clear existing data (optional, comment out if not needed)
        Faculty.objects.all().delete()
        Department.objects.all().delete()

        current_faculty = None
        faculty_pattern = re.compile(r'^(\w+)\s+(.+?)\s+\((\w+)\)$')

        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines
            if not line:
                i += 1
                continue

            # Check if this is a Faculty header
            if "Faculty of" in line or "School of" in line or "Institute of" in line or "College of" in line or "Centre for" in line:
                # Extract faculty code and title
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

                if next_line and len(next_line.split()) >= 2:
                    faculty_code = next_line.split()[0]

                    # Check if the next line is actually a department (has two codes)
                    parts = next_line.split()
                    if len(parts) >= 3 and len(parts[0]) <= 5 and len(parts[1]) <= 5:
                        # This is not a faculty code, use the current line
                        faculty_parts = line.split()
                        faculty_code = faculty_parts[0]
                        faculty_title = ' '.join(faculty_parts[1:])

                        # Create or update faculty
                        faculty, created = Faculty.objects.update_or_create(
                            code=faculty_code,
                            defaults={'title': faculty_title}
                        )
                        current_faculty = faculty

                        self.stdout.write(
                            f"{'Created' if created else 'Updated'} faculty: {faculty_code} - {faculty_title}")
                        i += 1
                    else:
                        faculty_title = line

                        # Create or update faculty
                        faculty, created = Faculty.objects.update_or_create(
                            code=faculty_code,
                            defaults={'title': faculty_title}
                        )
                        current_faculty = faculty

                        self.stdout.write(
                            f"{'Created' if created else 'Updated'} faculty: {faculty_code} - {faculty_title}")
                        i += 2  # Skip the faculty code line
                else:
                    # Just use the current line since we can't match the pattern
                    parts = line.split()
                    faculty_code = parts[0]
                    faculty_title = ' '.join(parts[1:])

                    faculty, created = Faculty.objects.update_or_create(
                        code=faculty_code,
                        defaults={'title': faculty_title}
                    )
                    current_faculty = faculty

                    self.stdout.write(
                        f"{'Created' if created else 'Updated'} faculty: {faculty_code} - {faculty_title}")
                    i += 1

            elif line and current_faculty and len(line.split()) >= 2:
                # This should be a department line
                parts = line.split()
                dept_code = parts[0]

                # Skip lines that look like faculty headings
                if "Faculty of" in line or "School of" in line or "Institute of" in line:
                    i += 1
                    continue

                # If the format is "CODE  Department of X (CODE)" or similar
                title_parts = parts[1:]
                title = ' '.join(title_parts)

                # Handle cases with department code in parentheses at the end
                if title.endswith(')') and '(' in title:
                    paren_index = title.rfind('(')
                    possible_code = title[paren_index + 1:-1]

                    # If this looks like the department code
                    if possible_code.isupper() and len(possible_code) <= 5:
                        title = title[:paren_index].strip()

                if current_faculty:
                    # Create or update department
                    department, created = Department.objects.update_or_create(
                        code=dept_code,
                        defaults={
                            'title': title,
                            'faculty': current_faculty
                        }
                    )

                    self.stdout.write(f"  {'Created' if created else 'Updated'} department: {dept_code} - {title}")

                i += 1
            else:
                # Skip lines we can't parse
                i += 1