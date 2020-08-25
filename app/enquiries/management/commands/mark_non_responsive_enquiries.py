from django.conf import settings
from django.core.management.base import BaseCommand
from app.enquiries.utils import mark_non_responsive_enquiries


class Command(BaseCommand):
    """
    Command is to mark enquries as 'Non-Responsive' if a company has not responded to the team and
    the enquiry has not been updated in six weeks.
    """

    help = """
        this command finds enquiries not edited in six weeks that have the 'Awaiting Response'
        enquiry stage and updates this to 'Non-Responsive'
    """

    def handle(self, *args, **options):
        mark_non_responsive_enquiries(expiry_weeks=settings.ENQUIRY_RESPONSIVENESS_PERIOD_WEEKS)

        self.stdout.write(
            self.style.SUCCESS(
                f"""
                    Successfully updated enquiries older than
                    {settings.ENQUIRY_RESPONSIVENESS_PERIOD_WEEKS} weeks
                """
            )
        )
