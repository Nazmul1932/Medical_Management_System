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

    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company, context={"request": request})

        serializer_data = serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        company_bank_details = CompanyBank.objects.filter(company_id=serializer_data["id"])
        companybank_details_serializers = CompanyBankSerializer(company_bank_details, many=True)
        serializer_data["company_bank"] = companybank_details_serializers.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

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


class CompanyOnlyViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):

        return Company.objects.all()


class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):

        try:

            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id = serializer.data['id']
            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                print(medicine_detail)
                medicine_detail["medicine_id"] = medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2 = MedicalDetailsSerializer(data=medicine_details_list, many=True, context={"request": request})
            serializer2.is_valid()
            serializer2.save()

            dict_response = {"error": False, "message": "Medicine Data Save Successfully"}
        except:

            dict_response = {"error": True, "message": "Error During Saving Medicine Data"}

        return Response(dict_response)

    def list(self, request):

        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine, many=True, context={"request": request})

        medicine_data = serializer.data
        new_medicine_list = []

        for medicine in medicine_data:
            medicine_details = MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
            medicine["medicine_details"] = medicine_details_serializers.data
            new_medicine_list.append(medicine)

        response_dict = {"error": False, "message": "All Medicine list data", "data": serializer.data}

        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, context={"request": request})

        serializer_data = serializer.data

        medicine_details = MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
        serializer_data["medicine_details"] = medicine_details_serializers.data

        return Response({"error": False, "message": "Single data Fetch", "data": serializer.data})

    def update(self,request,pk=None):
        queryset=Medicine.objects.all()
        medicine=get_object_or_404(queryset,pk=pk)
        serializer=MedicineSerializer(medicine,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()

        for salt_detail in request.data["medicine_details"]:
            if salt_detail["id"]==0:

                del salt_detail["id"]
                salt_detail["medicine_id"]=serializer.data["id"]
                serializer2 = MedicalDetailsSerializer(data=salt_detail,context={"request": request})
                serializer2.is_valid()
                serializer2.save()
            else:

                queryset2=MedicalDetails.objects.all()
                medicine_salt=get_object_or_404(queryset2,pk=salt_detail["id"])
                del salt_detail["id"]
                serializer3=MedicalDetailsSerializer(medicine_salt,data=salt_detail,context={"request":request})
                serializer3.is_valid()
                serializer3.save()
                print("UPDATE")

        return Response({"error":False,"message":"Data Has Been Updated"})


class CompanyAccountViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):

        try:

            serializer = CompanyAccountSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Account Data Save Successfully"}
        except:

            dict_response = {"error": True, "message": "Error During Saving Company Account Data"}

        return Response(dict_response)

    def list(self, request):

        company_account = CompanyAccount.objects.all()
        serializer = CompanyAccountSerializer(company_account, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All Company Account list data", "data": serializer.data}

        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = CompanyAccount.objects.all()
        company_account = get_object_or_404(queryset, pk=pk)
        serializer = CompanyAccountSerializer(company_account, context={"request": request})
        return Response({"error": False, "message": "Single data Fetch", "data": serializer.data})

    def update(self, request, pk=None):
        queryset = CompanyAccount.objects.all()
        company_account = get_object_or_404(queryset, pk=pk)
        serializer = CompanyAccountSerializer(company_account, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data has been updated"})

