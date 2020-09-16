import json

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from . import database_population
from ..models import Datapackage


class HomePageViewTest(TestCase):
    def test_get(self):
        c = Client()
        response = c.get(reverse('homepage'))

        self.assertEqual(response.status_code, 200)


class TestDatapackageUiView(TestCase):
    def test_datapackage_no_uuid(self):
        c = Client()

        response = c.get(reverse('datapackage-ui'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/static/datapackage-ui/index.html')

    def test_datapackage_uuid(self):
        c = Client()

        response = c.get(reverse('datapackage-ui') + '?load=this_is_a_potential_uuid')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/static/datapackage-ui/index.html?load=this_is_a_potential_uuid')


class TestDatapackageDetailView(TestCase):
    def test_datapackage_detail(self):
        c = Client()

        schema_text = b'This is a very special datapackage'
        schema = Datapackage.objects.create(schema=schema_text)

        response = c.get(reverse('datapackage-detail', kwargs={'uuid': schema.uuid}))

        self.assertEqual(response.status_code, 200)
        # This view had contained the full schema. Currently not
        # TODO: add more verification    tests
        # self.assertContains(response, schema_text)


class TestDatapackageListView(TestCase):
    def test_datapackage_list(self):
        datapackage = database_population.create_datapackage()
        collaborator = database_population.create_person()

        datapackage.collaborators.add(collaborator)

        c = Client()
        response = c.get(reverse('datapackage-list', kwargs={'collaborator_uuid': collaborator.uuid}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, collaborator.full_name)


class TestDatapackageAddCommentView(TestCase):
    def test_add_comment(self):
        datapackage = database_population.create_datapackage()
        collaborator = database_population.create_person()

        datapackage.collaborators.add(collaborator)

        self.assertEqual(Comment.objects.count(), 0)
        c = Client()
        response = c.post(reverse('datapackage-add-comment', kwargs={'uuid': datapackage.uuid}),
                          data={'text': 'This is a comment',
                                'author': collaborator.id,
                                'save': 'Add Comment'}
                          )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('datapackage-detail', kwargs={'uuid': datapackage.uuid}))
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.all()[0]

        self.assertEqual(comment.text, 'This is a comment')
        self.assertEqual(comment.author, collaborator)


class TestApiSchemaView(TestCase):
    def test_get(self):
        c = Client()

        schema_text = 'This is a schema test2'
        schema = Datapackage.objects.create(schema=schema_text)

        response = c.get(reverse('api-datapackage', kwargs={'uuid': schema.uuid}))

        self.assertEqual(response.content.decode('utf-8'), schema_text)

    def test_post(self):
        c = Client()

        schema_count_before_post = Datapackage.objects.all().count()

        response = c.post(reverse('api-datapackage'), data='This should be a frictionless datapackage schema',
                          content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Datapackage.objects.all().count(), schema_count_before_post + 1)

    def test_put(self):
        c = Client()

        schema = Datapackage.objects.create(schema='This is a schema test')

        new_schema = 'This is a modification'
        response = c.put(reverse('api-datapackage', kwargs={'uuid': schema.uuid}), data=new_schema,
                         content_type='application/json')

        self.assertEqual(response.status_code, 200)

        schema.refresh_from_db()

        self.assertEqual(schema.schema, new_schema)


class TestApiDatapackageMarkdown(TestCase):
    def test_get(self):
        c = Client()

        schema_text = json.dumps(database_population.datapackage_schema())
        schema = Datapackage.objects.create(schema=schema_text)

        response = c.get(reverse('api-datapackage-markdown', kwargs={'uuid': schema.uuid}))
        self.assertEqual(response['content-type'], 'text/plain; charset=UTF-8')
        self.assertEqual(response.status_code, 200)

        markdown = response.content.decode('utf-8')

        self.assertIn(r'This is the title of a dataset', markdown)


class TestApiDatapackagePdf(TestCase):
    def test_get(self):
        c = Client()

        schema_text = json.dumps(database_population.datapackage_schema())
        schema = Datapackage.objects.create(schema=schema_text)

        response = c.get(reverse('api-datapackage-pdf', kwargs={'uuid': schema.uuid}))
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertEqual(response.status_code, 200)

        pdf = response.content

        self.assertTrue(len(pdf) > 50000)
        self.assertTrue(pdf.startswith(b'%PDF-1.5'))
