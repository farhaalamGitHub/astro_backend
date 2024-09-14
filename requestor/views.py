from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import viewsets
from pprint import pprint


# Create your views here.


class RequestorView(viewsets.ModelViewSet):
    queryset = Requestor.objects.all()
    serializer_class = RequestorSerializer


class OrganizationView(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class GeometryView(viewsets.ModelViewSet):
    queryset = Geometry.objects.all()
    serializer_class = GeometrySerializer


class QuotationView(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
