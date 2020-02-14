from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, viewsets, status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers


class EnquiryList(APIView):
    """
    List all enquiries, or create a new enquiry.
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


class EnquiryDetail(APIView):
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
