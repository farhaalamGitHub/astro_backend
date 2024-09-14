from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(
    [
        Requestor,
        QuotationTestParameter,
        QuotationObjectDimension,
        Geometry,
        File,
    ]
)


class QuotationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "requestor",
        "date_created",
    ]


admin.site.register(Quotation, QuotationAdmin)


class QuotationDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "quotation",
        "test",
        "test_object",
        "test_object_quantity",
        "test_condition",
        "test_condition_value",
        "unit_dimension",
    ]


admin.site.register(QuotationDetail, QuotationDetailAdmin)
