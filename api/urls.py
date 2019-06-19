from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from api.views import (
    CompanyCreateView,
    CompanyDetails,
    CompanyAddressDetails,
    CompanyAddressView,
    CompanyDetailsBySearch,
    PostalCodeView,
)
urlpatterns = [
    path('', CompanyCreateView.as_view(), name="company"),
    path('companysearch', CompanyDetailsBySearch.as_view(), name='search'),
    path('company/<int:company_id>/',
         CompanyDetails.as_view(),
         name='company_info'),
    path('company/<int:company_id>/address/',
         CompanyAddressView.as_view(),
         name='company_address'),
    path('company/<int:company_id>/address/<int:address_id>/',
         CompanyAddressDetails.as_view(),
         name='specific_company_address'),
    path('postal_code/<int:size>/',
         PostalCodeView.as_view(),
         name="postal_code_size"),
    path(r'docs/', get_swagger_view(title='API'), name='swagger-api-docs'),
]
