from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers


class EnquiryListView(GenericAPIView):
    """
    List all enquiries.

    In GET: Returns a paginated list of enquiries
    using PageNumberPagination. This is the default
    pagination class as set globally in settings
    """

    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    serializer_class = serializers.EnquiryDetailSerializer

    def get_queryset(self):
        return models.Enquiry.objects.all()

    def get(self, request, format=None):
        enquiries = self.get_queryset()

        num_pages = 1
        if self.pagination_class:
            page_size = self.pagination_class.page_size
            num_pages = len(enquiries) // page_size
            if len(enquiries) % page_size:
                num_pages += 1

        paged_queryset = self.paginate_queryset(enquiries)
        if paged_queryset:
            serializer = self.get_serializer(paged_queryset, many=True)
            results = self.get_paginated_response(serializer.data)
        else:
            results = serializers.EnquiryDetailSerializer(enquiries, many=True)

        return Response(
            {
                "serializer": results.data,
                "page_range": list(range(num_pages + 1)),
                "current_page": request.query_params.get("page", "1"),
            },
            template_name="enquiry_list.html",
        )


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
