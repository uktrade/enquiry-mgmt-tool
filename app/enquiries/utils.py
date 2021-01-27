import logging
from datetime import datetime, timedelta, timezone
from distutils import util

from django.conf import settings
from django.db import transaction
from openpyxl import Workbook

from app.enquiries import ref_data
from app.enquiries.models import Enquirer, Enquiry, Owner

ENQUIRER_FIELDS = Enquirer._meta.get_fields()
ENQUIRY_FIELDS = Enquiry._meta.get_fields()
OWNER_FIELDS = Owner._meta.get_fields()

ENQUIRER_FIELD_NAMES = [f.name for f in ENQUIRER_FIELDS]
ENQUIRY_FIELD_NAMES = [f.name for f in ENQUIRY_FIELDS]
ENQUIRY_OWN_FIELD_NAMES = list(filter(lambda x: x != "enquirer", ENQUIRY_FIELD_NAMES))
OWNER_FIELD_NAMES = [f.name for f in OWNER_FIELDS]

EXPORT_FIELD_NAMES = ENQUIRY_OWN_FIELD_NAMES + ["enquirer_" + n for n in ENQUIRER_FIELD_NAMES]


def get_oauth_payload(request):
    """
    Extracts the user's |oauth|_ token from session

    :param request:
    :type request: django.http.HttpRequest
    """
    return request.session.get(settings.AUTHBROKER_TOKEN_SESSION_KEY, None)


def row_to_enquiry(row: dict) -> Enquiry:
    """
    Converts a CSV :data:`row` into a persisted :class:`app.enquiries.models.Enquiry` instance.

    :param row:
    :type row: dict

    :returns: :class:`app.enquiries.models.Enquiry`
    """
    row_data = row.copy()

    # FIXME: Use dict comprehension here
    # Extract enquirer fields
    enquirer_items = {}
    for key, value in row.items():
        if key.startswith("enquirer_"):
            value = row_data.pop(key)

            # this is an optional field so if the value is not available
            # then skip it to assign the specified default in model
            if key == "enquirer_request_for_call" and value == "":
                continue
            enquirer_items[key.split("_", 1)[1]] = value

    enquirer = Enquirer(**enquirer_items)

    # validate enquirer before saving -
    # https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.full_clean
    enquirer.full_clean()

    # this is an optional field, if the value is blank ensure it gets default choice
    if row_data.get("marketing_channel") == "":
        row_data["marketing_channel"] = ref_data.MarketingChannel.DEFAULT
    # if date_received is not provided, set it to now
    if not row_data.get("date_received"):
        row_data["date_received"] = datetime.now()

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
    Converts a CSV ``row`` into a ``dict`` representing
    :class:`app.enquiries.models.Enquiry` query `kwargs`
    e.g. ``enquiry__enquirer__first_name``.

    :param csv_row: The CSV row
    :type csv_row: dict

    :returns: ``dict`` of queryset filter `kwargs`
    """

    # build queryset filter params
    qs_kwargs = {key.replace("enquirer_", "enquirer__"): value for key, value in csv_row.items()}

    return qs_kwargs


def generate_import_template(file_obj):
    """
    Generates an |xlsx|_ spreadsheet for use by by `IST team` to capture enquiries.

    The main `enquiry` sheet is used by end users to capture information.
    The enquiry sheet columns are listed in :data:`app.enquiries.ref_data.IMPORT_COL_NAMES`.

    The additional sheets list valid options (i.e. Country names etc) which
    enable end users to implement their own form of validation.

    The fields for these sheets are also listed in :mod:`app.enquiries.ref_data`

    :param file_obj:
    :type file_obj: file-like object
    """
    ENTRY_SHEET_NAME = "enquiries"

    book = Workbook()

    references = [
        ref_data.Country,
        ref_data.EnquiryStage,
        ref_data.HowDidTheyHear,
        ref_data.InvestmentReadiness,
        ref_data.ISTSector,
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


def parse_error_messages(e):
    """
    Takes an error and parses its messages in human-readable form.

    Where there are message dictionaries, separates out each message,
    parsing the keys into sentence case with title capitalisations

    :param e:
    :type e: django.core.exceptions.ValidationError

    :returns: A list of error messages
    """
    response = []

    if hasattr(e, "message_dict"):
        for key, value in e.message_dict.items():
            msg = f'{key.replace("_", " ").title()}:'
            for v in value:
                msg += f" {v}"
            response.append(msg)
    else:
        response.append(str(e))

    return response


def mark_non_responsive_enquiries(expiry_weeks):
    past_date = datetime.now(timezone.utc) - timedelta(weeks=expiry_weeks)
    logging.info(f"Updating non-responsive enquiries from before {past_date}")

    entries = Enquiry.objects.select_for_update().filter(
        modified__lt=past_date, enquiry_stage=ref_data.EnquiryStage.AWAITING_RESPONSE
    )

    with transaction.atomic():
        for entry in entries:
            logging.info(f"Updating enquiry last updated on {entry.modified}")
            entry.enquiry_stage = ref_data.EnquiryStage.NON_RESPONSIVE
            entry.save()

    logging.info(f"Updated enquiry stage of {len(entries)} enquiries")


def str2bool(val=None):
    if val is None:
        return val
    return bool(util.strtobool(str(val)))
