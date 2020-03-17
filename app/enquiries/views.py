from django.db import transaction
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator as DjangoPaginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django_filters import rest_framework as filters

from rest_framework import generics, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers
from app.enquiries import forms

UNASSIGNED = "UNASSIGNED"

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
        This filter handles the owner__id parameter with can either be an int
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
        return context


class EnquiryEditView(LoginRequiredMixin, UpdateView):
    """
    View to provide complete details of an Enquiry
    """

    model = models.Enquiry
    form_class = forms.EnquiryForm
    template_name = "enquiry_edit.html"

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
