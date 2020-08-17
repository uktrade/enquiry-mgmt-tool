from django.core.management.base import BaseCommand
from django.db import transaction
from app.enquiries.models import Enquiry


class Command(BaseCommand):
    """
    Command is for one-off use to populate the date_received value for existing enquiries,
    replacing empty values with the date the record was created
    """

    help = "this command replaces empty date_received values for enquiries with the date created"

    def handle(self, *args, **options):
        print('Replacing empty date_received values')

        entries = Enquiry.objects.select_for_update().filter(date_received=None)
        with transaction.atomic():
            for entry in entries:
                entry.date_received = entry.created
                print(entry.date_received)
                entry.save()

        print(f'Updated {len(entries)} enquiries')
