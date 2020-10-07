from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "license_no", "address", "contact_no", "email", "description"]
