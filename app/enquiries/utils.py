from django.conf import settings
from openpyxl import Workbook

import app.enquiries.ref_data as ref_data
from app.enquiries.models import Enquirer, Enquiry



def get_oauth_payload(request):
    """
    Returns the Staff SSO oauth data stored in the session (i.e. oauth token, expiry time etc )
    (the oauth data is need for authentication with data and other services authenticated via Staff SSO)
    """
    return request.session.get(settings.AUTHBROKER_TOKEN_SESSION_KEY, None)


def row_to_enquiry(row: list) -> Enquirer:
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

    # validate enquirer before saving
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

    # save and associate
    enquirer.save()
    e.enquirer = enquirer
    e.save()
    return e


def generate_import_template(file_obj):
    """
    This function generates an .XLSX spreadsheet for use by by IST team to capture enquiries.
    The main sheet 'enquiries' is the one end users use to capture information.
    
    The enquiry sheet columns are listed in:
    
        app.enquiries.ref_data.py:IMPORT_COL_NAMES

    enquirer_first_name | enquirer_last_name | enquirer_job_title | enquirer_email | enquirer_phone | enquirer_request_for_call | country | company_name | primary_sector | company_hq_address | website | investment_readiness | enquiry_text | notes
    
    The additional sheets list valid options (i.e. Country names etc) which enable end users to implement their own form of validation.

    The fields for these sheets are also listed in ref_data.py

    """
    ENTRY_SHEET_NAME = "enquiries"

    book = Workbook()

    references = [
        ref_data.Country,
        ref_data.EnquiryStage,
        ref_data.HowDidTheyHear,
        ref_data.InvestmentReadiness,
        ref_data.PrimarySector,
        ref_data.RequestForCall,
    ]

    # setup enquiries sheet
    current_sheet = book.active
    current_sheet.title = ENTRY_SHEET_NAME
    current_sheet.append(ref_data.IMPORT_COL_NAMES)

    # append sheets containing ref data
    for ref in references:
        current_sheet = book.create_sheet(f"REF_{ref.__name__}")
        for choice in ref.choices:
            row = [str(v) for v in choice]
            current_sheet.append(row)
    book.save(file_obj)
