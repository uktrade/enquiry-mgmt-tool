from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
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
            {"serializer": serializer.data}, template_name="enquiry_list.html",
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
        context["owners"] = self.get_owners()
        return context
    
    def get_owners(self):
        owners = [
            {"id": "", "name": "Unassigned"}
        ]
        for owner in models.Owner.objects.all():
            owners.append({"id": owner.id, "name": str(owner.user.first_name) + " " + str(owner.user.last_name)})
        return owners


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
