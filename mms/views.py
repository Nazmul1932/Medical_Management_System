from django.shortcuts import render
from rest_framework import viewsets


# Create your views here.
from mms.models import *
from mms.serilizers import *


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
