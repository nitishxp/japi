import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from api.models import (
    Company,
    CompanyAddress,
)
from api.serializers import (
    CompanyAddressSerialzier,
    CompanyInfoSerializer,
)


class TodoListCreateAPIViewTestCase(APITestCase):
    url = reverse("api:company")

    def setUp(self):
        self.company = Company.objects.create(name='Test Company')
        self.company = Company.objects.create(name='abc')
        self.address = CompanyAddress.objects.create(company=self.company,
                                                     postal_code=111111,
                                                     city='Tokyo',
                                                     state='Japan')
        pincodes = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 9]
        for c in pincodes:
            CompanyAddress.objects.create(company=self.company,
                                          postal_code=c,
                                          city='Tokyo',
                                          state='Japan')

        self.company_address_url = reverse(
            'api:company_address', kwargs={'company_id': self.company.id})
        self.company_specific_address_url = reverse(
            'api:specific_company_address',
            kwargs={
                'company_id': self.company.id,
                'address_id': self.address.id
            })

    def test_create_company(self):
        response = self.client.post(self.url, {"name": "Test Company 1"})
        self.assertEqual(201, response.status_code)

    def test_create_company_address(self):
        response = self.client.post(
            self.company_address_url, {
                "building_number": "test building",
                "postal_code": "111111",
                "locality": "lko",
                "city": "tokyo",
                "state": "tokyo"
            })
        self.assertEqual(201, response.status_code)

    def test_company_address_update(self):
        response = self.client.put(
            self.company_specific_address_url, {
                "building_number": "test building",
                "postal_code": "111111",
                "locality": "lko",
                "city": "tokyo",
                "state": "India"
            })
        self.assertEqual(200, response.status_code)
        state = CompanyAddress.objects.get(pk=self.address.id)
        self.assertEqual(state.state, 'India')

    def test_company_address_delete(self):
        response = self.client.delete(self.company_specific_address_url)
        self.assertEqual(204, response.status_code)

    def test_company_by_name_or_city(self):
        response = self.client.get("{}?{}".format(reverse('api:search'),
                                                  "search=tokyo"))

        self.assertEqual(len(response.json()), 1)

        response = self.client.get("{}?{}".format(reverse('api:search'),
                                                  "search=abc"))

        self.assertEqual(len(response.json()), 1)

        response = self.client.get("{}?{}".format(reverse('api:search'),
                                                  "search=tok"))

        self.assertEqual(len(response.json()), 0)

    def test_pincode_size(self):

        response = self.client.get(
            reverse('api:postal_code_size', kwargs={'size': 0}))

        # since 6 different pincodes
        self.assertEqual(len(response.json()), 6)

        response = self.client.get(
            reverse('api:postal_code_size', kwargs={'size': 2}))

        # since 1,2,3,4
        self.assertEqual(len(response.json()), 4)

        response = self.client.get(
            reverse('api:postal_code_size', kwargs={'size': 10}))

        # none
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(
            reverse('api:postal_code_size', kwargs={'size': 4}))

        # only 4
        self.assertEqual(len(response.json()), 1)
