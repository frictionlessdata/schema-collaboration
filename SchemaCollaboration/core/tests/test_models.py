from django.test import TestCase
from django.urls import reverse

from core.models import Person, DatapackageStatus, Datapackage


class PersonTest(TestCase):
    def test_str(self):
        person = Person(full_name='John Doe')

        self.assertEqual(str(person), 'John Doe')

    def test_get_absolute_uri(self):
        person = Person(full_name='John Doe')
        person.save()

        self.assertEqual(person.get_absolute_url(),
                         reverse('management:person-detail', kwargs={'pk': person.pk}))


class DatapackageStatusTest(TestCase):
    def test_datapackage_status(self):
        status = DatapackageStatus(name='Draft')

        self.assertEqual(str(status), 'Draft')


class DatapackageTest(TestCase):
    def test_collaborators_excluding_str(self):
        datapackage = Datapackage.objects.create()

        person1 = Person.objects.create(full_name='Alan')
        person2 = Person.objects.create(full_name='James')

        datapackage.collaborators.add(person1, person2)

        self.assertEqual(datapackage.collaborators_excluding_str(person2), 'Alan')

    def test_get_absolute_uri(self):
        datapackage = Datapackage.objects.create()

        self.assertEqual(datapackage.get_absolute_url(), reverse('datapackage-detail',
                                                                 kwargs={'uuid': str(datapackage.uuid)}))

    def test_file_name_named(self):
        datapackage = Datapackage.objects.create(name='Microplastics')

        file_name = datapackage.file_name(extension='.pdf')

        self.assertIn('Microplastics', file_name)
        self.assertTrue(file_name.endswith('.pdf'))

    def test_file_name_unnamed(self):
        datapackage = Datapackage.objects.create()

        file_name = datapackage.file_name(extension='.pdf')

        self.assertIn('unnamed', file_name)
        self.assertTrue(file_name.endswith('.pdf'))

