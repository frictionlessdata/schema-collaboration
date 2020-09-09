from django.test import TestCase
from django.urls import reverse

from core.tests import database_population


class ViewsTest(TestCase):
    def setUp(self):
        self._management_client = database_population.create_management_logged_client()
        self._person = database_population.create_person()
        self._datapackage = database_population.create_datapackage()

    def test_list_schemas(self):
        response = self._management_client.get(reverse('management:list-schemas'))

        self.assertEqual(response.status_code, 200)

    def test_list_people(self):
        response = self._management_client.get(reverse('management:list-people'))

        self.assertEqual(response.status_code, 200)

    def test_person_create(self):
        response = self._management_client.get(reverse('management:person-add'))

        self.assertEqual(response.status_code, 200)

    def test_person_detail(self):
        response = self._management_client.get(reverse('management:person-detail', kwargs={'pk': self._person.pk}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Sheldon Cooper')

    def test_person_update(self):
        response = self._management_client.get(reverse('management:person-update', kwargs={'pk': self._person.pk}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Sheldon Cooper')

    def test_datapackage_detail(self):
        response = self._management_client.get(
            reverse('management:datapackage-detail', kwargs={'uuid': self._datapackage.uuid}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self._datapackage.name)

    def test_datapackage_update(self):
        response = self._management_client.get(
            reverse('management:datapackage-update', kwargs={'uuid': self._datapackage.uuid}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self._datapackage.name)
