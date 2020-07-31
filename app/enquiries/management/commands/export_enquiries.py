import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.enquiries.models import Enquiry
import app.enquiries.ref_data as ref_data

OUTPUT_FILE_SLUG = "ingest_sample"
OUTPUT_FILE_EXT = ".csv"


class Command(BaseCommand):
    """
    Command is for use by developers to quickly export CSV data so that the
    upload functionality can be easily tested.
    """

    help = "this command exports enquiries to simple (level) CSV"

    def handle(self, *args, **options):
        count = 0
        timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
        entries = Enquiry.objects.all().iterator()
        filename = f"{OUTPUT_FILE_SLUG}_{timestamp}{OUTPUT_FILE_EXT}"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            # write headers
            writer.writerow(ref_data.IMPORT_COL_NAMES)
            for e in entries:
                writer.writerow(
                    [
                        e.enquirer.first_name,
                        e.enquirer.last_name,
                        e.enquirer.job_title,
                        e.enquirer.email,
                        e.enquirer.phone,
                        e.enquirer.request_for_call,
                        e.country,
                        e.company_name,
                        e.ist_sector,
                        e.company_hq_address,
                        e.website,
                        e.investment_readiness,
                        e.enquiry_stage,
                        e.enquiry_text,
                        e.notes,
                    ]
                )
                count += 1
        # writer.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"""Successfully exported enquiry to simple (level 1)
            file: "{filename}" """
            )
        )
