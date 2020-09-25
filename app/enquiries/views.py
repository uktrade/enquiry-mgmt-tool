import csv
import json
import logging
from datetime import datetime
from io import BytesIO

from chardet import UniversalDetector
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVRenderer

from app.enquiries.common.datahub_utils import dh_investment_create
from app.enquiries import forms, models, serializers, utils
from app.enquiries.utils import (
    row_to_enquiry,
    get_oauth_payload,
    parse_error_messages,
)
from app.enquiries.common.datahub_utils import dh_company_search, dh_request


UNASSIGNED = "UNASSIGNED"


class DataHubAdviserSearch(LoginRequiredMixin, View):
    """
    Endpoint for the `Client Relationship Manager` autocomplete field
    of :class:`app.enquiries.forms.EnquiryForm`.
    """
    def get(self, request):
        session = get_oauth_payload(request)
        access_token = session["access_token"]

        res = dh_request(
            request,
            access_token,
            method="GET",
            url=settings.DATA_HUB_ADVISER_SEARCH_URL,
            params=dict(autocomplete=request.GET.get("q")),
        )

        try:
            data = res.json()
        except json.decoder.JSONDecodeError:
            data = {}

        return JsonResponse(
            dict(
                results=[
                    dict(text=adviser["name"], id=adviser["name"]) for adviser in data["results"]
                ]
            )
            if res.status_code == 200
            else data,
            status=res.status_code,
            reason=res.reason,
        )


def get_filter_config():
    filter_fields = [field for field in models.Enquiry._meta.get_fields() if field.choices]
    filter_config = {}
    for field in filter_fields:
        filter_config[field.name] = field
    return filter_config


def get_enquiry_field(name):
    filter_config = get_filter_config()

    return {"name": name, "choices": filter_config[name].choices}


class PaginationWithPaginationMeta(PageNumberPagination):
    """
    Adds additional metadata to the template context.
    """

    def get_paginated_response(self, data):
        response_data = {
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count,
            "current_page": self.page.number,
            "results": data,
            "filter_enquiry_stage": get_enquiry_field("enquiry_stage"),
            "owners": models.Owner.objects.all().order_by("first_name"),
            "query_params": self.request.GET,
            "total_pages": len(self.page.paginator.page_range),
            "sort_options": settings.ENQUIRY_SORT_OPTIONS,
            "pages": [
                {
                    "page_number": page_number,
                    "current": page_number == self.page.number,
                    "link": replace_query_param(self.request.get_full_path(), "page", page_number),
                }
                for page_number in self.page.paginator.page_range
            ],
        }
        return Response(truncate_response_data(response_data))

    def post(self, request):
        serializer = serializers.EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def truncate_response_data(response_data, block_size=4):
    """
    Truncates pagination links.

    We don't want to show a link for every page if there are lots of pages.
    This replaces page links which are less useful with an ``...`` ellipsis.

    :param response_data:
        Data supposed to be passed to :class:`rest_framework.response.Response`.
    :type response_data: dict

    :param block_size:
        How many page links should be kept at each end of the truncated portion.
    :type block_size: int

    :returns: The response data with updated ``'pages'`` key
    :rtype: dict
    """
    pages = response_data["pages"]

    if len(pages) <= block_size:
        return response_data

    current_page_num = response_data["current_page"]
    current_page_index = response_data["current_page"] - 1
    first_page = pages[0]
    last_page = pages[-1]

    block_pivot = block_size // 2
    start_of_current_block = abs(current_page_num - block_pivot)
    start_of_last_block = last_page["page_number"] - block_size
    block_start_index = min(start_of_current_block, start_of_last_block, current_page_index)

    truncated_pages = pages[block_start_index:][:block_size]
    first_of_truncated_pages_num = truncated_pages[0]["page_number"]
    last_of_truncated_pages_num = truncated_pages[-1]["page_number"]

    if first_of_truncated_pages_num > 3:
        truncated_pages = [{"page_number": "..."}] + truncated_pages

    if first_of_truncated_pages_num == 3:
        truncated_pages = [pages[1]] + truncated_pages

    if first_of_truncated_pages_num > 1:
        truncated_pages = [first_page] + truncated_pages

    if last_of_truncated_pages_num < last_page["page_number"] - 2:
        truncated_pages.append({"page_number": "..."})

    if last_of_truncated_pages_num == last_page["page_number"] - 2:
        truncated_pages.append(pages[-2])

    if last_of_truncated_pages_num < last_page["page_number"]:
        truncated_pages.append(last_page)

    response_data["pages"] = truncated_pages
    return response_data


def is_valid_id(v) -> bool:
    if v == UNASSIGNED:
        return True
    return is_valid_int(v)


def is_valid_int(v) -> bool:
    try:
        int(v)
    except ValueError:
        return False
    return True


class EnquiryFilter(filters.FilterSet):
    """
    Enquiry search filters
    """
    owner__id = filters.CharFilter(field_name="owner__id", method="filter_owner_id")
    received__lt = filters.DateFilter(field_name="receive", method="filter_received_lt")
    received__gt = filters.DateFilter(field_name="receive", method="filter_received_gt")
    enquiry_stage = filters.CharFilter(
        field_name="enquiry_stage", lookup_expr="in", method="filter_enquiry_stage"
    )
    enquirer__email = filters.CharFilter(field_name="enquirer__email", lookup_expr="icontains")

    def filter_enquiry_stage(self, queryset, name, value):
        values = self.request.GET.getlist(name)
        return queryset.filter(enquiry_stage__in=values)

    def filter_owner_id(self, queryset, name, value):
        """
        Handles the ``owner__id`` parameter which can either be an int
        or the string ``'UNASSIGNED'``. In the case of ``'UNASSIGNED'``
        to filter for enquirires where ``owner == None``.
        """
        vals = self.request.GET.getlist(name)
        # filter out valid values (int|'UNASSIGNED')
        valid_vals = list(filter(is_valid_id, vals))
        int_vals = list(filter(is_valid_int, valid_vals))
        # cast numbers to int
        int_vals = list(map(lambda v: int(v), int_vals))

        q = Q()

        if UNASSIGNED in valid_vals:
            q |= Q(owner__id__isnull=True)

        if int_vals:
            q |= Q(owner__id__in=int_vals)

        return queryset.filter(q)

    def filter_received_lt(self, queryset, name, value):
        """
        Returns a :class:`django.db.models.query.QuerySet` only with entities
        which have ``date_received`` less than ``value``.
        """
        received = datetime.combine(value, datetime.min.time())
        q = Q(date_received__lt=received)
        return queryset.filter(q)

    def filter_received_gt(self, queryset, name, value):
        """
        Returns a :class:`django.db.models.query.QuerySet` only with entities
        which have a ``date_received`` greater than ``value``.
        """
        received = datetime.combine(value, datetime.min.time())
        q = Q(date_received__gt=received)
        return queryset.filter(q)

    class Meta:
        model = models.Enquiry
        fields = {
            "company_name": ["icontains"],
            "date_added_to_datahub": ["lt", "gt"],
            "project_code": ["icontains"]
        }


class EnquiryListCSVRenderer(CSVRenderer):
    """
    A custom CSV renderer showing only selected fields.
    """

    header = settings.EXPORT_OUTPUT_FILE_CSV_HEADERS


class EnquiryListView(LoginRequiredMixin, ListAPIView):
    """
    The `enquiry search` view.
    """

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EnquiryFilter
    template_name = "enquiry_list.html"
    renderer_classes = (TemplateHTMLRenderer, EnquiryListCSVRenderer)
    serializer_class = serializers.EnquiryDetailSerializer
    pagination_class = PaginationWithPaginationMeta

    def get_queryset(self):
        sortby = self.request.query_params.get("sortby")
        all_enquiries = models.Enquiry.objects.all()

        return all_enquiries.order_by(
            sortby if sortby in settings.ENQUIRY_SORT_OPTIONS.keys() else "-date_received"
        )

    @property
    def is_csv(self):
        return self.request.query_params.get("format") == "csv"

    @property
    def paginator(self):
        """Disables pagination for ``?format=csv`` requests"""
        if self.is_csv:
            self._paginator = None

        return super().paginator

    def finalize_response(self, *args, **kwargs):
        """Handles the ``Content-Disposition`` header of a ``?format=csv`` request"""
        response = super().finalize_response(*args, **kwargs)

        if self.is_csv:
            fname = settings.EXPORT_OUTPUT_FILE_SLUG
            ext = settings.EXPORT_OUTPUT_FILE_EXT
            response["Content-Disposition"] = f"attachment; filename={fname}.{ext}"

        return response


class EnquiryCreateView(LoginRequiredMixin, APIView):
    """
    Creates new :class:`app.enquiries.models.Enquiry`
    """

    def post(self, request, format=None):
        serializer = serializers.EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnquiryDetailView(LoginRequiredMixin, TemplateView):
    """
    :class:`app.enquiries.models.Enquiry` detail view
    """

    model = models.Enquiry
    template_name = "enquiry_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enquiry = get_object_or_404(models.Enquiry, pk=kwargs["pk"])
        context["enquiry"] = enquiry
        context["back_url"] = reverse("index")
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        enquiry = context["enquiry"]

        create_response = dh_investment_create(request, enquiry)
        if create_response.get("result", {}).get("id"):
            enquiry.refresh_from_db()
            context["enquiry"] = enquiry
            context[
                "success"
            ] = f"Enquiry for {enquiry.company_name} successfully submitted to Data Hub"
        else:
            context["errors"] = create_response["errors"]
        response = render(request, self.template_name, context)
        response.status_code = (
            status.HTTP_400_BAD_REQUEST if create_response["errors"] else status.HTTP_201_CREATED
        )
        return response


class EnquiryEditView(LoginRequiredMixin, UpdateView):
    """
    :class:`app.enquiries.models.Enquiry` edit view
    """

    model = models.Enquiry
    form_class = forms.EnquiryForm
    template_name = "enquiry_edit.html"

    def get_context_data(self, **kwargs):
        # these are populated when a company is selected from the list of
        # search results in the company search view
        data = self.request.GET
        selected_company_id = data.get("dh_id")
        enquiry_obj = self.get_object()
        context = super().get_context_data(**kwargs)
        if selected_company_id:
            context["dh_company_id"] = selected_company_id
            context["dh_company_number"] = data.get("dh_number")
            context["dh_duns_number"] = data.get("duns_number")
            context["dh_assigned_company_name"] = data.get("dh_name")
            context["dh_company_address"] = data.get("dh_address")
        elif enquiry_obj.dh_company_id:
            context["dh_company_id"] = enquiry_obj.dh_company_id
            context["dh_company_number"] = enquiry_obj.dh_company_number
            context["dh_duns_number"] = enquiry_obj.dh_duns_number
            context["dh_assigned_company_name"] = enquiry_obj.dh_assigned_company_name
            context["dh_company_address"] = enquiry_obj.dh_company_address

        return context

    def form_valid(self, form):
        enquiry_obj = self.get_object()
        enquirer_form = forms.EnquirerForm(form.data, instance=enquiry_obj.enquirer)
        if enquirer_form.is_valid():
            enquirer = enquirer_form.save(commit=False)
            enquiry = form.save(commit=False)

            with transaction.atomic():
                enquirer.save()
                enquiry.save()
            return redirect("enquiry-detail", pk=enquiry.id)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        enquiry_obj = self.get_object()
        enquirer_form = forms.EnquirerForm(form.data, instance=enquiry_obj.enquirer)
        errors_dict = json.loads(enquirer_form.errors.as_json())
        for field, msg in errors_dict.items():
            form.add_error(None, field)
        response = super().form_invalid(form)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


class EnquiryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete :class:`app.enquiries.models.Enquiry` view
    """

    model = models.Enquiry
    template_name = "enquiry_delete.html"

    def post(self, *args, **kwargs):
        enquiry = get_object_or_404(models.Enquiry, pk=kwargs["pk"])
        enquiry.delete()
        return redirect("index")


class EnquiryCompanySearchView(LoginRequiredMixin, TemplateView):
    """|data-hub|_ company search view"""

    model = models.Enquiry
    template_name = "enquiry_company_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enquiry = get_object_or_404(models.Enquiry, pk=kwargs["pk"])
        context["enquiry"] = enquiry
        context["data_hub_create_company_page_url"] = settings.DATA_HUB_CREATE_COMPANY_PAGE_URL
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        search_term = request.POST["search_term"].lower()
        context["search_results"] = []
        companies, error = dh_company_search(self.request, None, search_term)
        if not error:
            for company in companies:
                addr = company["address"]
                formatted_addr = f'{company["name"]}, {addr["line_1"]}, \
                    {addr["line_2"]}, {addr["town"]}, {addr["county"]}, \
                    {addr["postcode"]}, {addr["country"]}'
                context["search_results"].append(
                    {
                        "datahub_id": company["datahub_id"],
                        "name": company["name"],
                        "company_number": company["company_number"],
                        "duns_number": company["duns_number"],
                        "address": formatted_addr,
                    }
                )

        return render(request, self.template_name, context)


class ImportEnquiriesView(LoginRequiredMixin, TemplateView):
    """
    Handles import of enquiries with a CSV file
    """

    http_method_names = ["get", "post"]
    ERROR_HEADER = "Error - File import has failed"

    @property
    def ERROR_URL(self):
        return reverse("import-enquiries") + "?errors=1"

    def _build_records(self, csv_lines):
        records = []
        if len(csv_lines) <= 1:
            raise Exception("Empty CSV file or only header row detected, no records imported")

        # import all or none
        with transaction.atomic():
            records = [row_to_enquiry(row) for row in csv.DictReader(csv_lines)]

        return records

    def process_upload(self, uploaded_file):
        records = []
        with uploaded_file as f:
            # Accumulate file content by reading in chunks
            # We should not process the chunk straightaway because depending on the
            # chunk size last line of csv could be partial
            buf = BytesIO()
            for c in f.chunks(chunk_size=settings.UPLOAD_CHUNK_SIZE):
                buf.write(c)

            encoding_detector = UniversalDetector()
            buf.seek(0)
            encoding_detector.feed(buf.read())
            detection_result = encoding_detector.close()
            encoding = detection_result["encoding"]
            logging.info(f"Encoding detection result: {detection_result}")

            # Use the encoding detected by chardet, in case of failure use utf-8
            try:
                buf.seek(0)
                decoded = buf.read().decode(encoding)
            except Exception:
                buf.seek(0)
                decoded = buf.read().decode("utf-8")
            finally:
                csv_lines = decoded.split("\n")

            records = self._build_records(csv_lines)

        logging.info(f"Successfully imported {len(records)} records")
        return records

    def post(self, request, *args, **kwargs):
        records = []
        enquiries_key = "enquiries"

        file_obj = request.FILES.get(enquiries_key)
        if not file_obj:
            messages.error(
                self.request, "No file was selected. Choose a file to upload.",
            )
            return HttpResponseRedirect(reverse("import-enquiries"))

        if not (
            file_obj.name.endswith(".csv")
            and file_obj.content_type in settings.IMPORT_ENQUIRIES_MIME_TYPES
        ):
            messages.error(
                self.request,
                f"Input file is not a CSV file, detected type: {file_obj.content_type}",
            )
            return HttpResponseRedirect(reverse("import-enquiries"))

        try:
            records = self.process_upload(file_obj)
        except ValidationError as err:
            for msg in parse_error_messages(err):
                messages.add_message(request, messages.ERROR, msg)
            logging.error(err)
            return HttpResponseRedirect(self.ERROR_URL)
        except Exception as err:
            messages.add_message(request, messages.ERROR, f"Unexpected error, {str(err)}")
            logging.error(err)
            return HttpResponseRedirect(self.ERROR_URL)

        return render(
            self.request,
            "import-enquiries-confirmation.html",
            {"enquiries": records, "ERROR_HEADER": self.ERROR_HEADER},
        )

    def get(self, request, *args, **kwargs):
        status_code = (
            status.HTTP_400_BAD_REQUEST if "errors" in request.GET else status.HTTP_200_OK
        )
        return render(
            request,
            "enquiry_import.html",
            {"ERROR_HEADER": self.ERROR_HEADER},
            status=status_code,
        )


class ImportTemplateDownloadView(LoginRequiredMixin, View):
    methods = ["get"]
    CONTENT_TYPE = settings.IMPORT_TEMPLATE_MIMETYPE

    def get(self, request):
        response = HttpResponse(content_type=self.CONTENT_TYPE)
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{settings.IMPORT_TEMPLATE_FILENAME}"'
        utils.generate_import_template(response)
        return response
