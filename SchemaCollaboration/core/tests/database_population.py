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


def create_person():
    person, created = Person.objects.get_or_create(full_name='Sheldon Cooper')
    return person


def create_datapackage():
    datapackage, created = Datapackage.objects.get_or_create(name='For the unit test',
                                                             schema='''This should contain a datapackage''')

    return datapackage