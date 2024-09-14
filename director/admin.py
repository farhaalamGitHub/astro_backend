from django.contrib import admin
from .models import *

# # Register your models here.


class AdminAdmin(admin.ModelAdmin):
    list_display = ["user_id", "phone_no"]


admin.site.register(
    [
        Admin,
        Alloy,
        TestCategory,
        Test,
        Condition,
        TestParameter,
        TestObject,
        StanderdTestObjectDimension,
    ]
)
