from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from django.db.transaction import set_autocommit

from core.models import Person


class Command(BaseCommand):
    help = 'Creates the data management user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('full_name', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        username = options['username']
        full_name = options['full_name']
        password = options['password']

        try:
            create_user_name(username, full_name, password)
        except IntegrityError:
            print('Could not create the data manager')

        print('Done!')


@transaction.atomic
def create_user_name(username, full_name, password):
    try:
        user = User.objects.create_user(username, password=password)
    except IntegrityError as e:
        print(f'Error: integrity error. Please check that the user "{username}" does not already exist')
        raise e

    try:
        person = Person.objects.create(full_name=full_name, user=user)
    except IntegrityError as e:
        print(f'Error: integrity error. Please make sure that a person with full_name="{full_name}" does already exist')
        raise e
