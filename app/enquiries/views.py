from django.http import QueryDict
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models.query import QuerySet
from functools import reduce
from operator import __and__ as AND
from rest_framework import generics, viewsets, status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers
from app.enquiries.ref_data import EnquiryStage
from django.db.models import Q

filter_props = {
    "enquiry_stage": "enquiry_stage__in",
    "owner": "owner__id__in",
    "company_name": "company_name__icontains",
    "enquirer_email": "enquirer__email",
    "date_created_before": "created__lt",
    "date_created_after": "created__gt",
    "date_added_to_datahub_before": "date_added_to_datahub__lt",
    "date_added_to_datahub_after": "date_added_to_datahub__gt",
}

def filter_queryset(queryset: QuerySet, query_params: QueryDict) -> QuerySet:
    multi_option_fields = ["enquiry_stage", "owner"]
    single_option_fields = [
        "company_name",
        "enquirer_email",
        "date_created_before",
        "date_created_after",
        "date_added_to_datahub_before",
        "date_added_to_datahub_before",
    ]

    filters = {}
    match_unassigned = False
    qobjs = Q()

    for k, v in query_params.items():
        if k in multi_option_fields and query_params.getlist(k):
            if k == "owner":
                users = []
                for user in query_params.getlist(k):
                    # handle UNASSIGNED value differently as this maps to a DB null value
                    if user == "UNASSIGNED":
                        match_unassigned = True
                    else:
                        users.append(user)
                if len(users) > 0:
                    filters[k] = users
            else:
                filters[k] = query_params.getlist(k)
        elif k in single_option_fields and query_params.get(k):
            filters[k] = v

    if filters.keys() or match_unassigned:
        for k, v in filters.items():
            if k == 'owner':
                # we need to group the owner queryies together using an OR operator
                if match_unassigned == True:
                    qobjs &= Q(Q(**{filter_props[k]: v}) | Q(owner__isnull=True))
                else:
                    qobjs &= Q(**{filter_props[k]: v})        
                continue
            qobjs &= Q(**{filter_props[k]: v})
        qs = queryset.filter(qobjs)
    else:
        qs = queryset
    return qs

class EnquiryListView(APIView):
    """
    List all enquiries.
    """

    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    def get_queryset(self) -> QuerySet:
        queryset = models.Enquiry.objects.all()
        return filtered_queryset(queryset, self.request.GET)

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
