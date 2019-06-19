import coreapi

from django.http import Http404
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    GenericAPIView,
)
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count
from api.models import (Company, CompanyAddress)
from api.serializers import (
    CompanyCreateSerializer,
    CompanyAddressSerialzier,
    CompanyInfoSerializer,
)


class CompanyCreateView(ListCreateAPIView):
    """
    get:
    Return list of companies

    post:
    Create a new company
    """
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer


class CompanyDetails(APIView):
    """
    get: 
    Return all info about a particular company id
    """
    schema = AutoSchema([
        coreapi.Field("company_id",
                      required=True,
                      location='path',
                      description='Enter Company id')
    ])

    def get_object(self, company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, company_id):
        obj = self.get_object(company_id)
        serializer = CompanyInfoSerializer(obj)
        return Response(serializer.data)


class CompanyDetailsBySearch(ListAPIView):
    """
    get:
    Returns all info of companies which are found in search result
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field("search",
                      required=True,
                      location='query',
                      description='Enter either city name or company name'),
    ])

    queryset = Company.objects.all()
    serializer_class = CompanyInfoSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', '=companyaddress__city')


class CompanyAddressView(APIView):
    """
    get:
    Returns all address of given company
    
    post:
    Add a new address to the given company
    """
    schema = AutoSchema([
        coreapi.Field("company_id",
                      required=True,
                      location='path',
                      description='Enter Company id')
    ])

    def get_serializer(self, *args, **kwargs):
        return CompanyAddressSerialzier()

    def get(self, request, company_id):
        queryset = CompanyAddress.objects.filter(company_id=company_id)
        serializer = CompanyAddressSerialzier(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, company_id):
        serializer = CompanyAddressSerialzier(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CompanyAddressDetails(APIView):
    """
    get:
    Returns the given address of a given company

    put:
    Update the given address of a given company

    delete:
    Delete the given address of a given company
    """
    schema = AutoSchema([
        coreapi.Field("company_id",
                      required=True,
                      location='path',
                      description='Enter Company id'),
        coreapi.Field("address_id",
                      required=True,
                      location='path',
                      description='Enter address id'),
    ])

    def get_serializer(self, *args, **kwargs):
        return CompanyAddressSerialzier()

    def get_object(self, company_id, address_id):
        try:
            return CompanyAddress.objects.get(pk=address_id,
                                              company_id=company_id)
        except CompanyAddress.DoesNotExist:
            raise Http404

    def get(self, request, company_id, address_id):
        obj = self.get_object(company_id, address_id)
        serializer = CompanyAddressSerialzier(obj)
        return Response(serializer.data)

    def put(self, request, company_id, address_id):
        obj = self.get_object(company_id, address_id)
        serializer = CompanyAddressSerialzier(obj, data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=company_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, address_id):
        obj = self.get_object(company_id, address_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostalCodeView(APIView):
    """
    get: List all Postal Code having address more then given size
    """
    schema = AutoSchema([
        coreapi.Field("size",
                      required=True,
                      location='path',
                      description='Enter size'),
    ])

    def get(self, request, size):
        r = CompanyAddress.objects.all().values('postal_code').annotate(
            total=Count('postal_code')).order_by('total').filter(
                total__gte=size)
        return Response(r)