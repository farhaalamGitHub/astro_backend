from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from .serializers import *
from .models import *

# Create your views here.

# ----------- Create view for Condition ------------


class ConditionView(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


# ----------- Create view for TestObject ------------


class TestObjectView(viewsets.ModelViewSet):
    queryset = TestObject.objects.all()
    serializer_class = TestObjectSerializer


# ----------- Create view for Test ------------


class TestView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class AlloyView(viewsets.ModelViewSet):
    queryset = Alloy.objects.all()
    serializer_class = AlloySerializer

    @action(detail=False, methods=["get"])
    def base_alloy(self, request):
        parent_alloys = Alloy.get_parent_level_alloys()
        serializer = self.get_serializer(parent_alloys, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def sub_alloy(self, request, pk=None):
        try:
            parent_alloy = self.get_object()

            children_alloys = Alloy.get_children_alloys(parent_alloy.id)

            if children_alloys is not None:
                serializer = self.get_serializer(children_alloys, many=True)
                return Response(serializer.data)
            else:
                return Response("Parent alloy not found")
        except Alloy.DoesNotExist:
            return Response("Parent alloy not found")


# ----------- Create view for TestCategory ----------


class TestCategoryView(viewsets.ModelViewSet):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer
