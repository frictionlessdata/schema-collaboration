from django.core.management.base import BaseCommand
from django.db import IntegrityError

from core.models import DatapackageStatus


class Command(BaseCommand):
    help = 'Creates default data package status'

    def add_arguments(self, parser):
        parser.add_argument('--only-if-no-status', action='store_true')

    def handle(self, *args, **options):
        if options['only_if_no_status'] and DatapackageStatus.objects.count() > 0:
            print('Database already contains status - doing nothing')
            return 1

        return create_status(['Draft', 'In Progress', 'Completed'])


def create_status(status_names):
    for status_name in status_names:
        try:
            DatapackageStatus.objects.create(name=status_name)
        except IntegrityError:
            print(f'Cannot create status name="{status_name}". Does already exist?')
            continue

        print(f'Created {status_name}')
        return 0