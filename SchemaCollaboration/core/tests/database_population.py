from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client


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
