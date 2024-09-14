from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"testObject", TestObjectView)
router.register(r"test", TestView)
router.register(r"condition", ConditionView)
router.register(r"alloys", AlloyView)
router.register(r"testCategory", TestCategoryView)

urlpatterns = [
    path("", include(router.urls)),
]
