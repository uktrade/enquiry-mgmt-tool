from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from enquiries import models, serializers


class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = models.Enquiry.objects.all()
    serializer_class = serializers.EnquirySerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def list(self, request, *args, **kwargs):
        response = super(EnquiryViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='enquiry_list.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(EnquiryViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'data': response.data}, template_name='enquiry_detail.html')
        return response
