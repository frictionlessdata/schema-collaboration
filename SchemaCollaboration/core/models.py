import uuid as uuid_lib

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class CreateModifyOn(models.Model):
    """Details of data creation and modification: including date, time and user."""
    objects = models.Manager()  # Helps Pycharm CE auto-completion

    created_on = models.DateTimeField(help_text='Date and time at which the entry was created', auto_now_add=True)
    modified_on = models.DateTimeField(help_text='Date and time at which the entry was modified', auto_now=True,
                                       blank=True, null=True)

    class Meta:
        abstract = True


class Person(CreateModifyOn):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('management:collaborator-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'People'


class DatapackageStatus(CreateModifyOn):
    class StatusBehaviour(models.TextChoices):
        DEFAULT_ON_DATAPACKAGE_CREATION = 'CREATION', 'Default on Creation'

    name = models.CharField(max_length=255, blank=True, unique=True)
    behaviour = models.CharField(max_length=9,
                                 choices=StatusBehaviour.choices,
                                 null=True, blank=True,
                                 unique=True)

    class Meta:
        verbose_name_plural = 'Datapackage statuses'

    def __str__(self):
        return self.name


class Datapackage(CreateModifyOn):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, unique=True)
    schema = models.TextField()
    name = models.CharField(max_length=500, default='', blank=True)
    collaborators = models.ManyToManyField(Person, blank=True)
    status = models.ForeignKey(DatapackageStatus, null=True, default='', on_delete=models.PROTECT)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '-'

    def collaborators_sorted(self):
        return self.collaborators.all().order_by('full_name')

    def collaborators_str(self):
        return self.collaborators_excluding_str(None)

    def collaborators_excluding_str(self, excluded_collaborator):
        collaborators_list = []

        for collaborator in self.collaborators.all().order_by('full_name'):
            if collaborator != excluded_collaborator:
                collaborators_list.append(collaborator.full_name)

        if collaborators_list:
            return ', '.join(collaborators_list)
        else:
            return '-'

    def comments_for_management(self):
        return self.comment_set.order_by('created_on')

    def comments_for_collaborators(self):
        return self.comment_set.filter(private=False).order_by('created_on')

    def file_name(self, *, extension):
        date = f'{self.modified_on:%Y%m%d-%H%M}'
        if self.name:
            name = f'{self.name.replace(" ", "_")}-{date}.{extension}'
        else:
            name = f'unnamed-{date}.{extension}'

        return name

    def generate_edit_link(self, path):
        return f'{reverse("datapackage-ui")}?load={self.uuid}&source={path}'

    def get_absolute_url(self):
        return reverse('datapackage-detail', kwargs={'uuid': str(self.uuid)})
