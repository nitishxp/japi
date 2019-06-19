from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedRelatedField,
)
from api.models import (
    Company,
    CompanyAddress,
)


class CompanyCreateSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyAddressSerialzier(ModelSerializer):
    class Meta:
        model = CompanyAddress
        exclude = ['company']


class CompanyInfoSerializer(ModelSerializer):
    address = SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'address']

    def get_address(self, obj):
        queryset = CompanyAddress.objects.filter(company=obj)
        return CompanyAddressSerialzier(queryset, many=True).data
