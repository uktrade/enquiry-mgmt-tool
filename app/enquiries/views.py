from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from rest_framework import generics, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers
from app.enquiries import forms


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

    def post(self, request, format=None):
        serializer = serializers.EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    form_class = forms.EnquiryForm
    template_name = "enquiry_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: perform company search here
        context["companies"] = get_companies()
        if self.dh_assigned_company is not '':
            context["dh_assigned_company_name"] = self.dh_assigned_company['name']
            context["dh_assigned_company_address"] = self.dh_assigned_company['address']
        return context

    def get(self, request, *args, **kwargs):
        dhacid = request.GET.get('dhacid', '')
        if dhacid is '':
            self.dh_assigned_company = ''
        else:
            self.dh_assigned_company = [c for c in get_companies() if dhacid in c["datahub_id"]][0]
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        enquiry = form.save(commit=False)
        enquiry.save()
        return redirect("enquiry-detail", pk=enquiry.pk)

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
        # TODO: perform company search here
        context["search_results"] = [
            c for c in get_companies() if search_term in c["name"].lower()
        ]
        return render(request, self.template_name, context)
