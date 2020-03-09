from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.response import Response
from rest_framework.views import APIView

from app.enquiries import models, serializers


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


class EnquiryListView(APIView, PaginationHandlerMixin):
    """
    List all enquiries.

    In GET: Returns a paginated list of enquiries
    """

    pagination_class = EnquiryListPagination
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)

    # This is mainly used for displaying page range in the template
    django_paginator_class = DjangoPaginator

    def get(self, request, format=None):
        enquiries = models.Enquiry.objects.all()
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

        return Response(
            {
                "serializer": serializer.data,
                "page_range": list(paginator.page_range),
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
