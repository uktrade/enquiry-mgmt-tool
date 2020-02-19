from django.http import QueryDict
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, viewsets, status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers


class EnquiryListView(APIView):
    """
    List all enquiries.
    """

    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    def get(self, request, format=None):
        enquiries = models.Enquiry.objects.all()
        serializer = serializers.EnquiryDetailSerializer(enquiries, many=True)
        return Response(
            {"serializer": serializer.data}, template_name="enquiry_list.html",
        )

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
