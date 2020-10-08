
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from mms.models import *
from mms.serilizers import *


class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):

        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company list data", "data": serializer.data}

        return Response(response_dict)

    def create(self, request):

        try:

            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Data Save Successfully"}

        except:

            dict_response = {"error": True, "message": "Error During Saving Company Data"}

        return Response(dict_response)

    def update(self, request, pk=None):

        try:

            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            dict_response = {"error": False, "message": "Successfully update Company Data"}

        except:

            dict_response = {"error": True, "message": "Error During update Company Data"}

        return Response(dict_response)


company_list = CompanyViewSet.as_view({'get': 'list'})
company_create = CompanyViewSet.as_view({'post': 'create'})
company_update = CompanyViewSet.as_view({'put': 'update'})


class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):

        try:

            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Bank Data Save Successfully"}
        except:

            dict_response = {"error": True, "message": "Error During Saving Company Bank Data"}

        return Response(dict_response)


    def list(self, request):

        company_bank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(company_bank, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company Bank list data", "data": serializer.data}

        return Response(response_dict)


    def retrieve(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        company_bank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(company_bank, context={"request": request})
        return Response({"error": False, "message": "Single data Fetch", "data": serializer.data})


    def update(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        company_bank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(company_bank, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data has been updated"})


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer
    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)



