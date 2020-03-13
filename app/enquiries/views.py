from django.db import transaction
from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
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
        context["back_url"]: reverse("enquiry-list")
        return context


class EnquiryEditView(UpdateView):
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

class EnquiryAdd(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if 'errors' in request.GET:
            messages.add_message(request, messages.ERROR, 'The selected file could not be uploaded - please try again.')
        elif 'success' in request.GET:
            messages.add_message(request, messages.SUCCESS, 'Please return back to the enquiry summary page.')
        return Response(
            {
                "data": "goes here",
                "back_url": reverse("enquiry-list"),
                "main_bar_right_btn": {
                    "text": "Template download",
                    'href': '',
                    'element': 'a'
                },
                # @TODO integration with real backend and errors
                # currently using query variables just to illustrate the different states (success|errors)
                'hasErrors': 'errors' in request.GET,
                'hasSuccess': 'success' in request.GET,
            },
            template_name="enquiry_import.html"
        )