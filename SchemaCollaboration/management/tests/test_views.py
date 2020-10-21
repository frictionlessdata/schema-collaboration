from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from core.tests import database_population


class ViewsTest(TestCase):
    def setUp(self):
        self._management_client = database_population.create_management_logged_client()
        self._person = database_population.create_person()
        self._datapackage = database_population.create_datapackage()

    def test_list_schemas(self):
        response = self._management_client.get(reverse('management:list-schemas'))

        self.assertEqual(response.status_code, 200)

    def test_list_collaborators(self):
        response = self._management_client.get(reverse('management:collaborator-list'))

        self.assertEqual(response.status_code, 200)

    def test_person_create(self):
        response = self._management_client.get(reverse('management:collaborator-add'))

        self.assertEqual(response.status_code, 200)

    def test_person_detail(self):
        response = self._management_client.get(reverse('management:collaborator-detail', kwargs={'pk': self._person.pk}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Sheldon Cooper')

    def test_person_update(self):
        response = self._management_client.get(reverse('management:collaborator-update', kwargs={'pk': self._person.pk}))

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

    def test_add_comment(self):
        datapackage = database_population.create_datapackage()
        collaborator = database_population.create_person()

        datapackage.collaborators.add(collaborator)

        self.assertEqual(Comment.objects.count(), 0)
        response = self._management_client.post(
            reverse('management:datapackage-add-comment', kwargs={'uuid': datapackage.uuid}),
            data={'text': 'This is a comment',
                  'save': 'Add Comment'}
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('management:datapackage-detail', kwargs={'uuid': datapackage.uuid}))
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.all()[0]

        self.assertEqual(comment.text, 'This is a comment')
