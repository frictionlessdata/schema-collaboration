from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from core.models import Person


class Command(BaseCommand):
    help = 'Creates the data management user and the admin user'

    def add_arguments(self, parser):
        parser.add_argument('datamanager_user_name', type=str)
        parser.add_argument('datamanager_full_name', type=str)
        parser.add_argument('datamanager_password', type=str)
        parser.add_argument('admin_password', type=str)

        parser.add_argument('--only-if-no-people', action='store_true')

    def handle(self, *args, **options):
        if options['only_if_no_people'] and Person.objects.count() > 0:
            print('There are people in the database - not creating anyone else')
            return 1

        if not check_options(options):
            return 1

        datamanager_username = options['datamanager_user_name']
        datamanager_full_name = options['datamanager_full_name']
        datamanager_password = options['datamanager_password']

        try:
            create_datamanager(datamanager_username, datamanager_full_name, datamanager_password)
        except IntegrityError:
            print('Could not create the data manager')

        User.objects.create_superuser('admin', password=options['admin_password'])
        print('Done!')
        return 0

def check_options(options):
    required_options = ['datamanager_user_name', 'datamanager_full_name', 'datamanager_password', 'admin_password']

    valid = True

    for required_option in required_options:
        if options[required_option] == '':
            valid = False
            print(f'{required_option} cannot be an empty string')

    return valid


@transaction.atomic
def create_datamanager(username, full_name, password):
    try:
        user = User.objects.create_user(username, password=password)
    except IntegrityError as e:
        print(f'Error: integrity error. Please check that the user "{username}" does not already exist')
        raise e

    try:
        Person.objects.create(full_name=full_name, user=user)
    except IntegrityError as e:
        print(f'Error: integrity error. Please make sure that a person with full_name="{full_name}" does already exist')
        raise e
