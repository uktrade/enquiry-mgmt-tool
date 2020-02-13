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

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        enquiries = models.Enquiry.objects.all()
        serializer = serializers.EnquiryDetailSerializer(enquiries, many=True)
        return Response(
            {"serializer": serializer.data},
            template_name="enquiry_list.html",
        )


class EnquiryDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "enquiry_detail.html"

    def get(self, request, pk):
        enquiry = get_object_or_404(models.Enquiry, pk=pk)
        serializer = serializers.EnquiryDetailSerializer(enquiry)
        return Response(
            {
                "serializer": serializer,
                "enquiry": enquiry,
                "style": {"template_pack": "rest_framework/vertical/"},
            }
        )
