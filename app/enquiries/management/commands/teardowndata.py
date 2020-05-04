from django.core.management.base import BaseCommand
from app.enquiries.models import Enquiry, Owner

class Command(BaseCommand):
    """
    Command is for use by developers to quickly export CSV data so that the upload functionality can be easily tested
    """
    help = 'this command exports enquiries to simple (level) CSV'

    def handle(self, *args, **options):
        Enquiry.objects.all().delete()
        Owner.objects.all().delete()
       