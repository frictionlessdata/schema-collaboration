from django.test import Client
from django.test import TestCase
from django.urls import reverse

from ..models import Schema


class ViewsTest(TestCase):
    def test_homepage(self):
        c = Client()
        response = c.get(reverse('homepage'))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        c = Client()

        schema_count_before_post = Schema.objects.all().count()

        response = c.post(reverse('api-schema'), data='This should be a frictionless schema',
                          content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Schema.objects.all().count(), schema_count_before_post + 1)

    def test_put(self):
        c = Client()

        schema = Schema.objects.create(schema='This is a schema test')

        new_schema = 'This is a modification'
        response = c.put(reverse('api-schema', kwargs={'uuid': schema.uuid}), data=new_schema,
                         content_type='application/json')

        self.assertEqual(response.status_code, 200)

        schema.refresh_from_db()

        self.assertEqual(schema.schema, new_schema)

    def test_get(self):
        c = Client()

        schema_text = 'This is a schema test2'
        schema = Schema.objects.create(schema=schema_text)

        response = c.get(reverse('api-schema', kwargs={'uuid': schema.uuid}))

        self.assertEqual(response.content.decode('utf-8'), schema_text)

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

    def test_schema_detail(self):
        c = Client()

        schema_text = b'This is a very special schema'
        schema = Schema.objects.create(schema=schema_text)

        response = c.get(reverse('schema-detail', kwargs={'uuid': schema.uuid}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, schema_text)
