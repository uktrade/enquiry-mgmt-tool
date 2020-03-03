from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models.query import QuerySet
from functools import reduce
from operator import __and__ as AND
from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers
from app.enquiries.ref_data import EnquiryStage
from django.db.models import Q

filter_props = {
    "enquiry_stage": "enquiry_stage__in",
    "owner": "owner__user__id__in",
    "company_name": "company_name__icontains",
    "enquirer_email": "enquirer__email",
    "date_created_before": "created__lt",
    "date_created_after": "created__gt",
    "date_added_to_datahub_before": "date_added_to_datahub__lt",
    "date_added_to_datahub_after": "date_added_to_datahub__gt",
}


def filter_queryset(queryset, query_params):
    valid_keys = filter_props.keys()
    Qs = Q()

    # add filters to queryset
    for query_key, query_value in query_params.items():
        if query_key in valid_keys and query_value != "":
            # get specific query param as a list (can be in the URL multiple times)
            QUERY_PARAM_VALUES = query_params.getlist(query_key)
            for keyVal in QUERY_PARAM_VALUES:
                if query_key == "owner" and keyVal == "UNASSIGNED":
                    keyVal = None
                p = {filter_props[query_key]: keyVal}
                Qs |= Q(**p)
    queryset = models.Enquiry.objects.filter(Qs)
    return queryset


def filtered_queryset(query_params):
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
    for k, v in query_params.items():
        if k in multi_option_fields and query_params.getlist(k):
            if k == "owner":
                users = [
                    None if user == "UNASSIGNED" else user
                    for user in query_params.getlist(k)
                ]
                filters[k] = users
            else:
                filters[k] = query_params.getlist(k)
        elif k in single_option_fields and query_params.get(k):
            filters[k] = v

    if filters.keys():
        qobjs = [Q(**{filter_props[k]: v}) for k, v in filters.items()]
        enquiries = models.Enquiry.objects.filter(reduce(AND, qobjs))
    else:
        enquiries = models.Enquiry.objects.all()

    return enquiries


class PaginationHandlerMixin:
    """
    Mixin for handling pagination in APIView
    """

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset, request):
        if self.paginator is None:
            return None
        paginated_response = self.paginator.paginate_queryset(
            queryset, request, view=self
        )
        return paginated_response

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class EnquiryListPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = settings.ENQUIRIES_PER_PAGE


class EnquiryList(APIView, PaginationHandlerMixin):
    """
    Display list all enquiries, or creates a new enquiry.

    In GET: Returns a paginated list of enquiries
    In POST: Creates a new enquiry
    """

    pagination_class = EnquiryListPagination
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    def get_queryset(self):
        queryset = models.Enquiry.objects.all()
        return filter_queryset(queryset, self.request.GET)

    # This is mainly used for displaying page range in the template
    django_paginator_class = DjangoPaginator

    def get(self, request, format=None):
        enquiries = filtered_queryset(request.query_params)
        paged_queryset = self.paginate_queryset(enquiries, request)
        page_size = self.pagination_class.page_size
        paginator = self.django_paginator_class(enquiries, page_size)
        if paged_queryset:
            paged_serializer = serializers.EnquiryDetailSerializer(
                paged_queryset, many=True
            )
            serializer = self.get_paginated_response(paged_serializer.data)
        else:
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
                "page_range": paginator.page_range,
                "current_page": request.query_params.get("page", "1"),
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
                "back_url": reverse("enquiry-detail", args=[kwargs["pk"]]),
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
