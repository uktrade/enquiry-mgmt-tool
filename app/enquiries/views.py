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

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, format=None):
        enquiries = models.Enquiry.objects.all()
        serializer = serializers.EnquiryDetailSerializer(enquiries, many=True)
        return Response(
            {"serializer": serializer.data},
            template_name="enquiry_list.html",
        )
