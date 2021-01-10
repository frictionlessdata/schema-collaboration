import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client

from core.models import Person, Datapackage


def create_management_user():
    try:
        user = User.objects.get(username='datamanager')
        return user
    except ObjectDoesNotExist:
        pass

    user = User.objects.create_user(username='datamanager', password='frictionless')

    return user


def create_management_logged_client():
    create_management_user()

    client = Client()
    client.login(username='datamanager', password='frictionless')
    return client


def create_external_collaborator():
    person, created = Person.objects.get_or_create(full_name='External collaborator')
    return person


def create_person():
    person, created = Person.objects.get_or_create(full_name='Sheldon Cooper',
                                                   user=User.objects.get(username=create_management_user()))
    return person


def create_datapackage():
    datapackage, created = Datapackage.objects.get_or_create(name='For the unit test',
                                                             schema='''This should contain datapackage''')

    return datapackage


def datapackage_schema():
    datapackage = json.loads('''{
  "profile": "tabular-data-package",
  "resources": [
    {
      "name": "resource1",
      "profile": "tabular-data-resource",
      "schema": {}
    }
  ],
  "keywords": [
    "a",
    "b",
    "c"
  ],
  "name": "This is the name of the dataset",
  "title": "This is the title of a dataset",
  "description": "A very interesting dataset",
  "homepage": "https://google.com",
  "version": "1.0.2",
  "contributors": [
    {
      "title": "marie bloe",
      "role": "author"
    }
  ],
  "licenses": [
    {
      "name": "CC-BY-4.0",
      "title": "Creative Commons Attribution 4.0",
      "path": "https://creativecommons.org/licenses/by/4.0/"
    }
  ]
}''')

    return datapackage
