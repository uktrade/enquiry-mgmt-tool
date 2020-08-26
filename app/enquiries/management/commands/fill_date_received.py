import logging

from django.core.management.base import BaseCommand
from app.enquiries.models import Enquiry


class Command(BaseCommand):
    """
    Populates the :attr:`app.enquiries.models.Enquiry.date_received` of existing enquiries,
    replacing empty values with the date the record was created.
    """

    help = "Replaces empty date_received values for enquiries with the date created"

    def handle(self, *args, **options):
        logging.info('Replacing empty date_received values')

        updated = 0
        failed = 0
        for entry in Enquiry.objects.filter(date_received=None):
            try:
                entry.date_received = entry.created
                entry.save()
                updated += 1
                logging.info(f'Enquiry({entry.id}).date_received = {entry.date_received}')
            except Exception as e:
                failed += 1
                logging.error(f'Enquiry({entry.id}).date_received update failed')
                raise e

        logging.info(f'Enquiries updated: {updated}, failed: {failed}')
