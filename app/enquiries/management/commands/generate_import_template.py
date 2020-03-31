from django.core.management.base import BaseCommand, no_translations
from django.conf import settings
from openpyxl import Workbook
from app.enquiries.utils import generate_import_template

class Command(BaseCommand):
    help = '''this command generates a .XLSX template for users to enter enquiries
     and manually import them as a CSVfile'''

    def handle(self, *args, **options):
        generate_import_template(settings.IMPORT_TEMPLATE_FILENAME)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated the template file to: "{OUTPUT_FILE_NAME}"'))

