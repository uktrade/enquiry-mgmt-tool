import csv
import io
import typing

from django.conf import settings

from openpyxl import Workbook

import app.enquiries.ref_data as ref_data
from app.enquiries.models import Enquirer, Enquiry


from django.db.models import QuerySet

from app.enquiries import models, serializers


ENQUIRER_FIELDS = models.Enquirer._meta.get_fields()
ENQUIRY_FIELDS = models.Enquiry._meta.get_fields()
OWNER_FIELDS = models.Owner._meta.get_fields()

ENQUIRER_FIELD_NAMES = [f.name for f in ENQUIRER_FIELDS]
ENQUIRY_FIELD_NAMES = [f.name for f in ENQUIRY_FIELDS]
ENQUIRY_OWN_FIELD_NAMES = list(filter(lambda x: x != "enquirer", ENQUIRY_FIELD_NAMES))
OWNER_FIELD_NAMES = [f.name for f in OWNER_FIELDS]

EXPORT_FIELD_NAMES = ENQUIRY_OWN_FIELD_NAMES + [
    "enquirer_" + n for n in ENQUIRER_FIELD_NAMES
]


def get_oauth_payload(request):
    """
    Returns the Staff SSO oauth data stored in the session (i.e. oauth token, expiry time etc )
    (the oauth data is need for authentication with data and other services authenticated via Staff SSO)
    """
    return request.session.get(settings.AUTHBROKER_TOKEN_SESSION_KEY, None)


def row_to_enquiry(row: dict) -> Enquirer:
    """
    Takes an dict representing a CSV row and create an Enquiry instance before saving it to the db
    """
    row_data = row.copy()

    # Extract enquirer fields
    enquirer_items = {}
    for key, value in row.items():
        if key.startswith("enquirer_"):
            value = row_data.pop(key)

            # this is an optional field so if the value is not available
            # then skip it to assign the specified default in model
            if key == "enquirer_request_for_call" and value == "":
                continue
            enquirer_items[key.split('_', 1)[1]] = value

    enquirer = models.Enquirer(**enquirer_items)

    # validate enquirer before saving - https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.full_clean
    enquirer.full_clean()

    # this is an optional field, if the value is blank ensure it gets default choice
    if row_data.get("marketing_channel") == "":
        row_data["marketing_channel"] = ref_data.MarketingChannel.DEFAULT

    enquiry = Enquiry(enquirer=enquirer, **row_data)

    # validate enquiry before saving (but exclude enquirer)
    enquiry.full_clean(["enquirer"])

    # now that both enquiry and enquirer are valid we can save and associate them
    enquirer.save()
    enquiry.enquirer = enquirer
    enquiry.save()
    return enquiry


def csv_row_to_enquiry_filter_kwargs(csv_row: dict) -> dict:
    """
    Takes a dict (represents a CSV row as exported by the tool ) and returns a dict representing a model query
    i.e. enquiry__enquirer__first_name to access -> enquiry.enquirer.first_name
    """

    # build queryset filter params
    qs_kwargs = {
        key.replace("enquirer_", "enquirer__"): value for key, value in csv_row.items()
    }

    return qs_kwargs


def generate_import_template(file_obj):
    """
    This function generates an .XLSX spreadsheet for use by by IST team to capture enquiries.
    The main sheet 'enquiries' is the one end users use to capture information.
    
    The enquiry sheet columns are listed in:
    
        app.enquiries.ref_data.py:IMPORT_COL_NAMES

    enquirer_first_name | enquirer_last_name | enquirer_job_title | enquirer_email | enquirer_phone | enquirer_request_for_call | country | company_name | primary_sector | company_hq_address | website | investment_readiness | enquiry_stage | enquiry_text | notes
    
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
        ref_data.MarketingChannel,
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


def enquiry_to_dict(e: models.Enquiry) -> dict:
    output = {}

    for f in ENQUIRY_FIELDS:
        if f.name == "enquirer":
            output.update(enquirer_to_dict(getattr(e, f.name)))
        else:
            output[f.name] = getattr(e, f.name)

    return output


def enquirer_to_dict(e: models.Enquirer) -> dict:
    output = {}

    for f in ENQUIRER_FIELDS:
        col_name = "enquirer_" + f.name
        output[col_name] = getattr(e, f.name)

    return output


def export_to_csv(qs: QuerySet, fp: typing.IO):
    """
    Exports a CSV dump of the enquiries to a CSV file
    :qs: Django queryset
    :fp: file-like object. This includes Django HTTP response object
    :return: void
    """
    output = []
    writer = csv.DictWriter(fp, fieldnames=EXPORT_FIELD_NAMES)
    writer.writeheader()

    for e in qs.iterator():
        data = enquiry_to_dict(e)
        output.append(data)
        writer.writerow(data)
