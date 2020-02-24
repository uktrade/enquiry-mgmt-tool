from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models.query import QuerySet
from rest_framework import generics, viewsets, status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers
from app.enquiries.ref_data import EnquiryStage
<<<<<<< HEAD
from django.db.models import Q
=======
>>>>>>> add filters to list view

FILTER_PROPS_MAP = {
    "enquiry_stage": "enquiry_stage",
    "owner": "owner__user__id",
    "company_name": "company_name__icontains",
    "enquirer_email": "enquirer__email",
    "date_created_before": "created__lt",
    "date_created_after": "created__gt",
    "date_added_to_datahub_before": "date_added_to_datahub__lt",
    "date_added_to_datahub_after": "date_added_to_datahub__gt"
}

def filter_queryset(queryset: QuerySet, query_params: QueryDict):
    VALID_KEYS = FILTER_PROPS_MAP.keys()
    Qs = Q()
    # add filters to queryset
    for query_key, query_value in query_params.items():
        if query_key in VALID_KEYS and query_value != "":
            # get specific query param as a list (can be in the URL multiple times)
            QUERY_PARAM_VALUES = query_params.getlist(query_key)
            for keyVal in QUERY_PARAM_VALUES:
                # if query_key.startswith('date_'):
                #     p = {FILTER_PROPS_MAP[query_key]: keyVal + 'T00:00:00Z'}
                # else:
                #     p = {FILTER_PROPS_MAP[query_key]: keyVal}
                p = {FILTER_PROPS_MAP[query_key]: keyVal}
                Qs |= Q(**p)
    queryset = models.Enquiry.objects.filter(Qs)
    return queryset

class EnquiryListView(APIView):
    """
    List all enquiries.
    """

    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    def get_queryset(self):
        filterable = (
            'enquiry_stage', 'owner', 'company_name__icontains', 'enquirer_email',
            'created__lt', 'created__gt', 'date_added_to_datahub__lt',
            'date_added_to_datahub__gt', 'owner__user__id'
            )
        # filterable_dates = (
        #     'created__lt', 'created__gt', 'date_added_to_datahub__lt',
        #     'date_added_to_datahub__gt')
        queryset = models.Enquiry.objects.all()
        # add filters to queryset
        for key, value in self.request.query_params.items():
            if key in filterable and value != '':
                p = {key: value}
                queryset = queryset.filter(**p)
        return queryset

    def get_queryset(self):
        queryset = models.Enquiry.objects.all()
        return filter_queryset(queryset, self.request.GET)

    def get(self, request, format=None):
        enquiries = self.get_queryset()
        serializer = serializers.EnquiryDetailSerializer(enquiries, many=True)

<<<<<<< HEAD
        filter_fields = [
            field for field in models.Enquiry._meta.get_fields() if field.choices
        ]
=======
        filter_fields = [field for field in models.Enquiry._meta.get_fields() if field.choices]
>>>>>>> add filters to list view
        filter_config = {}
        for field in filter_fields:
            filter_config[field.name] = field
        return Response(
            {
                "serializer": serializer.data,
<<<<<<< HEAD
                "owners": models.Owner.objects.all(),
                "filters": filter_config,
                "query_params": request.GET,
=======
                'owners': models.Owner.objects.all(),
                'EnquiryStage': EnquiryStage(),
                'filters': filter_config,
                "query_params": request.GET
>>>>>>> add filters to list view
            },
            template_name="enquiry_list.html",
        )

    def post(self, request, format=None):
        serializer = serializers.EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnquiryDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        enquiry = get_object_or_404(models.Enquiry, pk=pk)
        serializer = serializers.EnquiryDetailSerializer(enquiry)
        return Response(
            {
                "serializer": serializer,
                "enquiry": enquiry,
                "style": {"template_pack": "rest_framework/vertical/"},
                "back_url": reverse("enquiry-list"),
            },
            template_name="enquiry_detail.html",
        )

    def get_edit_view(self, request, *args, **kwargs):
        enquiry = get_object_or_404(models.Enquiry, pk=kwargs["pk"])
        serializer = serializers.EnquirySerializer(enquiry)
        response = Response(
            {
                "pk": kwargs["pk"],
                "serializer": serializer,
                "enquiry": enquiry,
                "style": {"template_pack": "rest_framework/vertical/"},
                "back_url": reverse("enquiry-list"),
            },
            template_name="enquiry_edit.html",
        )
        response.accepted_renderer = TemplateHTMLRenderer()
        response.accepted_media_type = "text/html"
        response.renderer_context = self.get_renderer_context()
        return response

    def post(self, request, pk):
        enquiry = get_object_or_404(models.Enquiry, pk=pk)
        serializer = serializers.EnquirySerializer(
            enquiry, data=request.data, partial=True
        )
        if not serializer.is_valid():
            response = Response(
                {
                    "pk": pk,
                    "serializer": serializer,
                    "style": {"template_pack": "rest_framework/vertical/"},
                },
                template_name="enquiry_edit.html",
            )
            response.accepted_renderer = TemplateHTMLRenderer()
            response.accepted_media_type = "text/html"
            response.renderer_context = self.get_renderer_context()
            return response

        serializer.save()
        return redirect("enquiry-detail", pk=pk)

    def dispatch(self, request, *args, **kwargs):
        url = request.get_full_path()
        if url.split("/")[-1] == "edit":
            if request.method == "GET":
                return self.get_edit_view(request, *args, **kwargs)
            elif request.method == "POST":
                request.data = request.POST
                return self.post(request, kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)
