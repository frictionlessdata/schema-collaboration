from django.test import Client
from django.test import TestCase
from django.urls import reverse


class ViewsTest(TestCase):
    def test_homepage(self):
        c = Client()
        response = c.get(reverse('homepage'))

        self.assertEqual(response.status_code, 200)
