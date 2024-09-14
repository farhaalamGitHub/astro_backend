from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"Requestor", RequestorView)
router.register(r"Organization", OrganizationView)
router.register(r"file", FileView)
router.register(r"geometry", GeometryView)
router.register(r"quotation", QuotationView)


urlpatterns = [path("", include(router.urls))]
