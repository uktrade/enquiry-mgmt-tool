import app.enquiries.ref_data as ref_data
from app.enquiries.models import Enquirer, Enquiry


def row_to_enquiry(row: dict) -> Enquirer:
    """
    Takes an list representing a CSV row and create an Enquiry instance before saving it to the db
    """
    enquirer = Enquirer(
        first_name=row["enquirer_first_name"],
        last_name=row["enquirer_last_name"],
        job_title=row["enquirer_job_title"],
        email=row["enquirer_email"],
        phone=row["enquirer_phone"],
        request_for_call=row["enquirer_request_for_call"],
    )

    # validate enquirer before saving - https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.full_clean
    enquirer.full_clean()

    e = Enquiry(
        enquirer=enquirer,
        country=row["country"],
        company_name=row["company_name"],
        primary_sector=row["primary_sector"],
        company_hq_address=row["company_hq_address"],
        website=row["website"],
        investment_readiness=row["investment_readiness"],
        enquiry_text=row["enquiry_text"],
        notes=row["notes"],
    )

    # validate enquiry before saving (but exclude enquirer)
    e.full_clean(["enquirer"])

    # now that both enquiry and enquirer are valid we can save and associate them
    enquirer.save()
    e.enquirer = enquirer
    e.save()
    return e
