from django.contrib import admin

from app.enquiries.models import Enquiry, Enquirer, Owner


def all_fields_of(model, exclude=()):
    return [field.name for field in
            model._meta.fields if field.name not in exclude]


@admin.register(Enquirer)
class EnquirerAdmin(admin.ModelAdmin):
    list_display = all_fields_of(Enquirer)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = all_fields_of(Owner, ("password",))


@admin.display(
    description="Enquirer",
)
def enquirer(obj):
    return f"{obj.enquirer.first_name} {obj.enquirer.last_name}"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("owner", enquirer, "region", "country", "enquiry_stage",
                    "datahub_project_status", "date_received",
                    "date_added_to_datahub", "primary_sector", "project_code",
                    "project_name")
