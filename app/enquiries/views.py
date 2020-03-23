import codecs
import csv
import logging

from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator as DjangoPaginator

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

import app.enquiries.ref_data as ref_data
from app.enquiries import models, serializers
from app.enquiries.utils import row_to_enquiry


logger = logging.getLogger(__name__)


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
            }
        )


class EnquiryListView(ListAPIView):
    """
    List all enquiries.

    In GET: Returns a paginated list of enquiries using PageNumberPagination.
    This is the default pagination class as set globally in settings. It is
    also inherited via a meta class to add additional metadata required
    for use in the template
    """

    template_name = "enquiry_list.html"
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    serializer_class = serializers.EnquiryDetailSerializer
    pagination_class = PaginationWithPaginationMeta

    def get_queryset(self):
        return models.Enquiry.objects.all()


class EnquiryCreateView(APIView):
    """
    Creates new Enquiry
    """

    def post(self, request, format=None):
        serializer = serializers.EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnquiryDetailView(TemplateView):
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
        return context


class EnquiryEditView(UpdateView):
    """
    View to provide complete details of an Enquiry
    """

    model = models.Enquiry
    fields = "__all__"
    template_name = "enquiry_edit.html"

    def form_valid(self, form):
        enquiry = form.save(commit=False)
        enquiry.save()
        return redirect("enquiry-detail", pk=enquiry.pk)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


class ImportEnquiriesView(TemplateView):
    """
    View handles submission of CSV files containing enquiries
    """

    http_method_names = ["get", "post"]
    ERROR_HEADER = "Error - File import has failed"

    @property
    def ERROR_URL(self):
        return reverse("import-enquiries") + "?errors=1"

    def process_upload(self, uploaded_file):
        records = []
        with uploaded_file as f:
            if not f.name.endswith(".csv") or f.content_type != "text/csv":
                messages.error(
                    self.request,
                    f"File is not of type: text/csv with  extension .csv. Detected type: {f.content_type}",
                )
                return HttpResponseRedirect(reverse("import-enquiries"))
            with transaction.atomic():
                for c in f.chunks(chunk_size=settings.UPLOAD_CHUNK_SIZE):
                    csv_file = csv.DictReader(codecs.iterdecode(BytesIO(c), "utf-8"))
                    for row in csv_file:
                        records.append(row_to_enquiry(row))
        logger.info(f"Successfully ingested {len(records)} records")
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
            logger.error(err)
            return HttpResponseRedirect(self.ERROR_URL)
        return render(
            self.request,
            "import-enquiries-confirmation.html",
            {"enquiries": records, "ERROR_HEADER": self.ERROR_HEADER},
        )

    def get(self, request, *args, **kwargs):
        status_code = 400 if "errors" in request.GET else 200
        return render(
            request,
            "import-enquiries-form.html",
            {"ERROR_HEADER": self.ERROR_HEADER},
            status=status_code,
        )

