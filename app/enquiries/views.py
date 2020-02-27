from django.http import QueryDict
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models.query import QuerySet
from rest_framework import generics, viewsets, status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers
from app.enquiries.ref_data import EnquiryStage
from django.db.models import Q

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
                if query_key.startswith('date_'):
                    p = {FILTER_PROPS_MAP[query_key]: keyVal + 'T00:00:00Z'}
                else:
                    p = {FILTER_PROPS_MAP[query_key]: keyVal}
                # Qs.add(Q(**p), Q.OR)
                Qs |= Q(**p)
    queryset = models.Enquiry.objects.filter(Qs)
    return queryset

class EnquiryListView(APIView):
    """
    List all enquiries.
    """

    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    def get_queryset(self):
        queryset = models.Enquiry.objects.all()
        return filter_queryset(queryset, self.request.GET)

    def get(self, request, format=None):
        enquiries = self.get_queryset()
        serializer = serializers.EnquiryDetailSerializer(enquiries, many=True)

        filter_fields = [
            field for field in models.Enquiry._meta.get_fields() if field.choices
        ]
        filter_config = {}
        for field in filter_fields:
            filter_config[field.name] = field
        return Response(
            {
                "serializer": serializer.data,
                "owners": models.Owner.objects.all(),
                # "EnquiryStage": EnquiryStage(),
                "filters": filter_config,
                "query_params": request.GET,
            },
            template_name="enquiry_list.html",
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
