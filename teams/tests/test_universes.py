from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from crawler.models import Source


class UniversesListAPIViewTestCase(APITestCase):
    @property
    def url(self):
        return reverse("universes-list")

    def setUp(self):
        self.sources = baker.make(Source, _quantity=10)

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res_data = res.json()
        expected_data = [{"universe": source.name} for source in self.sources]

        self.assertEqual(expected_data, res_data)
