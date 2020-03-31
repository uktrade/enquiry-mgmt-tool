import codecs
import csv
import logging

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator as DjangoPaginator
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django_filters import rest_framework as filters
from io import BytesIO

from rest_framework import generics, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

import app.enquiries.ref_data as ref_data
from app.enquiries import forms, models, serializers, utils
from app.enquiries.utils import row_to_enquiry
from app.enquiries.common.datahub_utils import dh_company_search

UNASSIGNED = "UNASSIGNED"


def get_companies():
    return [
        {
            "datahub_id": "4859",
            "name": "ALPHABET PROJECTS UK LTD",
            "company_number": "87654",
            "duns_number": "abc345",
            "address": "Alphabet Projects UK Ltd, 50 High Street, London, United Kingdom",
        },
        {
            "datahub_id": "7575",
            "name": "ALPHABET PROJECTS INC",
            "company_number": "87876",
            "duns_number": "abc456",
            "address": "Alphabet Projects Inc, 50 Main Street, New York, United States",
        },
        {
            "datahub_id": "9685",
            "name": "ALPHABET PROJECTS DEUTSCHLAND GMBH",
            "company_number": "87887",
            "duns_number": "abc567",
            "address": "Alphabet Projects DE GMBH, Hauptstraße 50, Berlin, Germany",
        },
    ]


def get_filter_config():
    filter_fields = [
        field for field in models.Enquiry._meta.get_fields() if field.choices
    ]
    filter_config = {}
    for field in filter_fields:
        filter_config[field.name] = field
    return filter_config


def get_enquiry_field(name):
    filter_config = get_filter_config()

    return {
        "name": name,
        "choices": filter_config[name].choices
    }


class PaginationWithPaginationMeta(PageNumberPagination):
    """
    Metadata class to add additional metadata for use in template
    """

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "page_range": list(self.page.paginator.page_range),
                "current_page": self.page.number,
                "results": data,
                "filter_enquiry_stage": get_enquiry_field("enquiry_stage"),
                "owners": models.Owner.objects.all(),
                "query_params": self.request.GET,
            },
            template_name="enquiry_list.html",
        )

    def post(self, request, format=None):
        serializer = serializers.EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    owner__id = filters.CharFilter(field_name="owner__id", method="filter_owner_id")

    def filter_owner_id(self, queryset, name, value):
        """
        This filter handles the owner__id parameter which can either be an int
        of the string 'UNASSIGNED'. In the case of UNASSIGNED to filter for enquirires where owner == None
        """
        vals = value.split(",")
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

    class Meta:
        model = models.Enquiry
        fields = {
            "company_name": ["icontains"],
            "enquirer__email": ["exact"],
            "enquiry_stage": ["exact"],
            "created": ["lt", "gt"],
            "date_added_to_datahub": ["lt", "gt"],
        }


class EnquiryListView(LoginRequiredMixin, ListAPIView):
    """
    List all enquiries.

    In GET: Returns a paginated list of enquiries using PageNumberPagination.
    This is the default pagination class as set globally in settings. It is
    also inherited via a meta class to add additional metadata required
    for use in the template
    """

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EnquiryFilter
    template_name = "enquiry_list.html"
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    serializer_class = serializers.EnquiryDetailSerializer
    pagination_class = PaginationWithPaginationMeta

    def get_queryset(self):
        return models.Enquiry.objects.all()


class EnquiryCreateView(LoginRequiredMixin, APIView):
    """
    Creates new Enquiry
    """

    def post(self, request, format=None):
        serializer = serializers.EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnquiryDetailView(LoginRequiredMixin, TemplateView):
    """
    View to provide complete details of an Enquiry
    """

    model = models.Enquiry
    template_name = "enquiry_detail.html"

    def get_context_data(self, **kwargs):
        pk = kwargs["pk"]
        context = super().get_context_data(**kwargs)
        enquiry = get_object_or_404(models.Enquiry, pk=kwargs["pk"])
        context["enquiry"] = enquiry
        context["back_url"] = reverse("enquiry-list")
        return context


class EnquiryEditView(LoginRequiredMixin, UpdateView):
    """
    View to provide complete details of an Enquiry
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

    # def get(self, request, *args, **kwargs):
    #     dhacid = request.GET.get('dhacid', '')
    #     if dhacid is '':
    #         self.dh_assigned_company = ''
    #     else:
    #         self.dh_assigned_company = [c for c in get_companies() if dhacid in c["datahub_id"]][0]
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     return self.render_to_response(self.get_context_data(form=form))

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
        response = super().form_invalid(form)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


class EnquiryCompanySearchView(TemplateView):
    """
    Company search view
    """

    model = models.Enquiry
    template_name = "enquiry_company_search.html"

    def get_context_data(self, **kwargs):
        pk = kwargs["pk"]
        context = super().get_context_data(**kwargs)
        enquiry = get_object_or_404(models.Enquiry, pk=kwargs["pk"])
        context["enquiry"] = enquiry
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        search_term = request.POST["search_term"].lower()
        context["search_results"] = []
        companies, error = dh_company_search(search_term)
        print(companies)
        print(error)
        if not error:
            for company in companies:
                addr = company["address"]
                formatted_addr = f'{company["name"]}, {addr["line_1"]}, {addr["line_2"]}, {addr["town"]}, {addr["county"]}, {addr["postcode"]}, {addr["country"]}'
                context["search_results"].append({
                    "datahub_id": company["datahub_id"],
                    "name": company["name"],
                    "company_number": company["company_number"],
                    "duns_number": company["duns_number"],
                    "address": formatted_addr,
                })
        print(context["search_results"])

        return render(request, self.template_name, context)


class ImportEnquiriesView(TemplateView):
    """
    View handles submission of CSV files containing enquiries
    """

    http_method_names = ["get", "post"]
    ERROR_HEADER = "Error - File import has failed"

    @property
    def ERROR_URL(self):
        return reverse("import-enquiries") + "?errors=1"

    def _build_records(self, file_obj):
        records = []
        with transaction.atomic():
            for c in file_obj.chunks(chunk_size=settings.UPLOAD_CHUNK_SIZE):
                csv_file = csv.DictReader(codecs.iterdecode(BytesIO(c), "utf-8"))
                for row in csv_file:
                    records.append(row_to_enquiry(row))

        return records

    def process_upload(self, uploaded_file):
        records = []
        with uploaded_file as f:
            if not f.name.endswith(".csv") or f.content_type != "text/csv":
                messages.error(
                    self.request,
                    f"File is not of type: text/csv with  extension .csv. Detected type: {f.content_type}",
                )
                return HttpResponseRedirect(reverse("import-enquiries"))

            records = self._build_records(f)

        logging.info(f"Successfully ingested {len(records)} records")
        return records

    def post(self, request, *args, **kwargs):
        records = []
        enquiries_key = "enquiries"

        try:
            if enquiries_key in request.FILES:
                payload = (
                    request.FILES.get(enquiries_key)
                )
                records = self.process_upload(payload)
            else:
                messages.error(request, f"File is not detected")
                return HttpResponseRedirect(self.ERROR_URL)
        except Exception as err:
            messages.add_message(request, messages.ERROR, str(err))
            logging.error(err)
            return HttpResponseRedirect(self.ERROR_URL)
        return render(
            self.request,
            "import-enquiries-confirmation.html",
            {"enquiries": records, "ERROR_HEADER": self.ERROR_HEADER},
        )

    def get(self, request, *args, **kwargs):
        status_code = status.HTTP_400_BAD_REQUEST if "errors" in request.GET else status.HTTP_200_OK
        return render(
            request,
            "import-enquiries-form.html",
            {"ERROR_HEADER": self.ERROR_HEADER},
            status=status_code,
        )


class ImportTemplateDownloadView(View):
    methods = ["get"]
    CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def get(self, request):
        response = HttpResponse(content_type=self.CONTENT_TYPE)
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{settings.IMPORT_TEMPLATE_FILENAME}"'
        utils.generate_import_template(response)
        return response
