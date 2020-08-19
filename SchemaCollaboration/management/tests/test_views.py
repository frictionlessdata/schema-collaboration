from django.test import TestCase
from django.urls import reverse

from core.tests.database_population import create_management_logged_client


class ViewsTest(TestCase):
    def setUp(self):
        self._management_client = create_management_logged_client()

    def test_list_schemas(self):
        response = self._management_client.get(reverse('management:list-schemas'))

        self.assertEqual(response.status_code, 200)
